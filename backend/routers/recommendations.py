"""
Recommendation routes: personalized topics, knowledge gaps, adaptive path
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import User
from backend.schemas import RecommendationResponse, KnowledgeGapResponse
from backend.auth import get_current_user
from backend.ml.recommendations import recommend_topics
from backend.ml.knowledge_gaps import detect_knowledge_gaps
from backend.ml.adaptive_path import get_adaptive_recommendations

router = APIRouter()

@router.get("/topics", response_model=List[RecommendationResponse])
def get_topic_recommendations(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized topic recommendations using cosine similarity
    """
    recommendations = recommend_topics(current_user.id, db, limit)
    
    result = []
    for rec in recommendations:
        result.append(RecommendationResponse(
            topic_id=rec["topic_id"],
            topic_title=rec["topic_title"],
            difficulty_level=rec["difficulty_level"],
            recommendation_reason=rec["reason"],
            confidence_score=rec["similarity_score"]
        ))
    
    return result

@router.get("/knowledge-gaps", response_model=List[KnowledgeGapResponse])
def get_knowledge_gaps(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Detect knowledge gaps using Logistic Regression
    """
    gaps = detect_knowledge_gaps(current_user.id, db)
    
    result = []
    for gap in gaps:
        result.append(KnowledgeGapResponse(
            topic_id=gap["topic_id"],
            topic_title=gap["topic_title"],
            difficulty_level=gap["difficulty_level"],
            is_weak=gap["is_weak"],
            risk_score=gap["risk_score"]
        ))
    
    return result

@router.get("/adaptive-path", response_model=List[RecommendationResponse])
def get_adaptive_learning_path(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get adaptive learning path recommendations (rule-based)
    """
    recommendations = get_adaptive_recommendations(current_user.id, db)
    
    result = []
    for rec in recommendations:
        result.append(RecommendationResponse(
            topic_id=rec["topic_id"],
            topic_title=rec["topic_title"],
            difficulty_level=rec["difficulty_level"],
            recommendation_reason=rec["reason"],
            confidence_score=0.8 if rec["priority"] == "high" else 0.6
        ))
    
    return result
