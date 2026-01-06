"""
Adaptive learning path using rule-based logic
"""
from sqlalchemy.orm import Session
from typing import List, Dict
from backend.models import User, Topic, QuizAttempt, Course

def get_adaptive_recommendations(user_id: int, db: Session) -> List[Dict]:
    """
    Generate adaptive learning path based on rules:
    - Low score (< 60) → recommend easier content
    - High score (>= 80) → recommend next difficulty level
    - Failed twice → recommend revision
    """
    # Get all quiz attempts for user
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
    
    # Group attempts by topic
    topic_performance = {}
    for attempt in attempts:
        quiz = attempt.quiz
        topic_id = quiz.topic_id
        
        if topic_id not in topic_performance:
            topic_performance[topic_id] = {
                "scores": [],
                "attempts": 0,
                "topic": quiz.topic
            }
        
        topic_performance[topic_id]["scores"].append(attempt.score)
        topic_performance[topic_id]["attempts"] += 1
    
    recommendations = []
    
    # Rule 1: Low score → recommend easier content
    for topic_id, data in topic_performance.items():
        topic = data["topic"]
        avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
        
        if avg_score < 60:
            # Find easier topics in same course
            course_topics = db.query(Topic).filter(
                Topic.course_id == topic.course_id,
                Topic.order_index < topic.order_index
            ).order_by(Topic.order_index.desc()).limit(2).all()
            
            for easier_topic in course_topics:
                recommendations.append({
                    "topic_id": easier_topic.id,
                    "topic_title": easier_topic.title,
                    "difficulty_level": easier_topic.difficulty_level,
                    "reason": f"Low score on '{topic.title}' - review easier content",
                    "priority": "high"
                })
    
    # Rule 2: High score → recommend next difficulty level
    for topic_id, data in topic_performance.items():
        topic = data["topic"]
        avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
        
        if avg_score >= 80:
            # Find next topics in same course
            next_topics = db.query(Topic).filter(
                Topic.course_id == topic.course_id,
                Topic.order_index > topic.order_index
            ).order_by(Topic.order_index).limit(2).all()
            
            for next_topic in next_topics:
                recommendations.append({
                    "topic_id": next_topic.id,
                    "topic_title": next_topic.title,
                    "difficulty_level": next_topic.difficulty_level,
                    "reason": f"Excellent performance on '{topic.title}' - ready for next level",
                    "priority": "medium"
                })
            
            # Also recommend topics of next difficulty level
            difficulty_order = {"Beginner": "Intermediate", "Intermediate": "Advanced", "Advanced": None}
            next_difficulty = difficulty_order.get(topic.difficulty_level)
            
            if next_difficulty:
                advanced_topics = db.query(Topic).filter(
                    Topic.difficulty_level == next_difficulty,
                    Topic.course_id == topic.course_id
                ).limit(1).all()
                
                for adv_topic in advanced_topics:
                    recommendations.append({
                        "topic_id": adv_topic.id,
                        "topic_title": adv_topic.title,
                        "difficulty_level": adv_topic.difficulty_level,
                        "reason": f"Ready for {next_difficulty} level content",
                        "priority": "medium"
                    })
    
    # Rule 3: Failed twice → recommend revision
    for topic_id, data in topic_performance.items():
        topic = data["topic"]
        failed_attempts = sum(1 for score in data["scores"] if score < 60)
        
        if failed_attempts >= 2:
            recommendations.append({
                "topic_id": topic.id,
                "topic_title": topic.title,
                "difficulty_level": topic.difficulty_level,
                "reason": f"Multiple failed attempts - revision recommended",
                "priority": "high"
            })
    
    # Remove duplicates
    seen = set()
    unique_recommendations = []
    for rec in recommendations:
        if rec["topic_id"] not in seen:
            seen.add(rec["topic_id"])
            unique_recommendations.append(rec)
    
    # Sort by priority
    priority_order = {"high": 0, "medium": 1, "low": 2}
    unique_recommendations.sort(key=lambda x: priority_order.get(x.get("priority", "low"), 2))
    
    return unique_recommendations
