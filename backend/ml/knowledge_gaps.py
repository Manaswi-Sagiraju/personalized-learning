"""
Knowledge gap detection using Logistic Regression
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.models import User, Topic, QuizAttempt, Performance

def prepare_features(user_id: int, db: Session) -> pd.DataFrame:
    """
    Prepare feature matrix for knowledge gap detection
    Features: average_score, attempts_count, time_spent, difficulty_level
    """
    # Get all quiz attempts for user
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
    
    # Get performance data
    performances = db.query(Performance).filter(Performance.user_id == user_id).all()
    performance_dict = {p.topic_id: p.time_spent_minutes for p in performances}
    
    # Group attempts by topic
    topic_data = {}
    for attempt in attempts:
        quiz = attempt.quiz
        topic_id = quiz.topic_id
        
        if topic_id not in topic_data:
            topic_data[topic_id] = {
                "scores": [],
                "attempts": 0,
                "topic_id": topic_id
            }
        
        topic_data[topic_id]["scores"].append(attempt.score)
        topic_data[topic_id]["attempts"] += 1
    
    # Build feature matrix
    features = []
    labels = []
    topic_ids = []
    
    for topic_id, data in topic_data.items():
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            continue
        
        avg_score = np.mean(data["scores"]) if data["scores"] else 0
        attempts_count = data["attempts"]
        time_spent = performance_dict.get(topic_id, 0)
        
        # Difficulty encoding
        difficulty_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
        difficulty = difficulty_map.get(topic.difficulty_level, 1)
        
        # Features: [avg_score, attempts_count, time_spent, difficulty]
        features.append([avg_score, attempts_count, time_spent, difficulty])
        
        # Label: 1 if weak (score < 60), 0 if strong
        labels.append(1 if avg_score < 60 else 0)
        topic_ids.append(topic_id)
    
    if not features:
        return pd.DataFrame(), []
    
    df = pd.DataFrame(features, columns=["avg_score", "attempts_count", "time_spent", "difficulty"])
    return df, topic_ids, labels

def detect_knowledge_gaps(user_id: int, db: Session) -> List[Dict]:
    """
    Detect knowledge gaps using Logistic Regression
    """
    # Prepare features
    features_df, topic_ids, labels = prepare_features(user_id, db)
    
    if len(features_df) == 0:
        return []
    
    # Train logistic regression model
    if len(set(labels)) < 2:
        # Not enough data for training - use rule-based approach
        gaps = []
        for idx, topic_id in enumerate(topic_ids):
            topic = db.query(Topic).filter(Topic.id == topic_id).first()
            if not topic:
                continue
            
            avg_score = features_df.iloc[idx]["avg_score"]
            is_weak = avg_score < 60
            risk_score = max(0, min(1, (60 - avg_score) / 60))
            
            gaps.append({
                "topic_id": topic_id,
                "topic_title": topic.title,
                "difficulty_level": topic.difficulty_level,
                "is_weak": is_weak,
                "risk_score": float(risk_score)
            })
        return gaps
    
    # Scale features
    scaler = StandardScaler()
    features_scaled = scaler.fit_transform(features_df)
    
    # Train model
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(features_scaled, labels)
    
    # Predict probabilities
    probabilities = model.predict_proba(features_scaled)
    risk_scores = probabilities[:, 1]  # Probability of being weak
    
    # Get all topics user has attempted
    gaps = []
    for idx, topic_id in enumerate(topic_ids):
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            continue
        
        is_weak = labels[idx] == 1
        risk_score = float(risk_scores[idx])
        
        gaps.append({
            "topic_id": topic_id,
            "topic_title": topic.title,
            "difficulty_level": topic.difficulty_level,
            "is_weak": is_weak,
            "risk_score": risk_score
        })
    
    # Also check topics user hasn't attempted but should know about
    all_topics = db.query(Topic).all()
    attempted_topic_ids = set(topic_ids)
    
    for topic in all_topics:
        if topic.id not in attempted_topic_ids:
            # New topic - medium risk
            gaps.append({
                "topic_id": topic.id,
                "topic_title": topic.title,
                "difficulty_level": topic.difficulty_level,
                "is_weak": True,
                "risk_score": 0.5
            })
    
    # Sort by risk score (descending)
    gaps.sort(key=lambda x: x["risk_score"], reverse=True)
    
    return gaps
