"""
Content-based recommendation system using Cosine Similarity
"""
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.models import User, Topic, QuizAttempt, Performance

def get_user_topic_vector(user_id: int, db: Session) -> Dict[int, float]:
    """
    Create a feature vector for user based on quiz scores per topic
    Returns dict: {topic_id: average_score}
    """
    # Get all quiz attempts for user
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
    
    # Group by topic and calculate average scores
    topic_scores = {}
    for attempt in attempts:
        quiz = attempt.quiz
        topic_id = quiz.topic_id
        
        if topic_id not in topic_scores:
            topic_scores[topic_id] = []
        topic_scores[topic_id].append(attempt.score)
    
    # Calculate average scores
    topic_vectors = {}
    for topic_id, scores in topic_scores.items():
        topic_vectors[topic_id] = np.mean(scores)
    
    return topic_vectors

def get_topic_features(topic: Topic) -> np.ndarray:
    """
    Create feature vector for a topic based on difficulty level
    """
    difficulty_map = {"Beginner": 1.0, "Intermediate": 2.0, "Advanced": 3.0}
    difficulty_value = difficulty_map.get(topic.difficulty_level, 1.0)
    
    # Feature vector: [difficulty_level, order_index_normalized]
    return np.array([difficulty_value, topic.order_index / 10.0])

def recommend_topics(user_id: int, db: Session, limit: int = 5) -> List[Dict]:
    """
    Recommend topics using content-based filtering with cosine similarity
    """
    # Get user's performance vector
    user_vector = get_user_topic_vector(user_id, db)
    
    # Get all topics
    all_topics = db.query(Topic).all()
    
    if not all_topics:
        return []
    
    # Get topics user hasn't completed or scored poorly on
    completed_topic_ids = set(user_vector.keys())
    
    recommendations = []
    
    for topic in all_topics:
        # Skip if user already completed with high score
        if topic.id in user_vector and user_vector[topic.id] >= 80:
            continue
        
        # Get topic features
        topic_features = get_topic_features(topic)
        
        # Calculate similarity based on user's performance pattern
        if user_vector:
            # Create user preference vector based on completed topics
            user_preference = np.array([np.mean(list(user_vector.values())) / 100.0, 0.5])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                [user_preference],
                [topic_features]
            )[0][0]
        else:
            # New user - recommend beginner topics
            similarity = 1.0 if topic.difficulty_level == "Beginner" else 0.5
        
        # Determine recommendation reason
        if topic.id not in completed_topic_ids:
            reason = "New topic based on your learning pattern"
        elif user_vector.get(topic.id, 0) < 60:
            reason = "Weak area - needs revision"
        else:
            reason = "Continue learning path"
        
        recommendations.append({
            "topic_id": topic.id,
            "topic_title": topic.title,
            "difficulty_level": topic.difficulty_level,
            "similarity_score": float(similarity),
            "reason": reason
        })
    
    # Sort by similarity score (descending)
    recommendations.sort(key=lambda x: x["similarity_score"], reverse=True)
    
    return recommendations[:limit]
