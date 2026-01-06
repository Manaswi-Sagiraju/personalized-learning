"""
Student performance tracking routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Performance, User, Topic
from backend.schemas import PerformanceUpdate, PerformanceResponse
from backend.auth import get_current_user

router = APIRouter()

@router.post("/track", response_model=PerformanceResponse)
def track_performance(performance_data: PerformanceUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Track or update time spent on a topic
    """
    # Check if performance record exists
    performance = db.query(Performance).filter(
        Performance.user_id == current_user.id,
        Performance.topic_id == performance_data.topic_id
    ).first()
    
    if performance:
        # Update existing record
        performance.time_spent_minutes += performance_data.time_spent_minutes
    else:
        # Create new record
        performance = Performance(
            user_id=current_user.id,
            topic_id=performance_data.topic_id,
            time_spent_minutes=performance_data.time_spent_minutes
        )
        db.add(performance)
    
    db.commit()
    db.refresh(performance)
    return performance

@router.get("/user", response_model=List[PerformanceResponse])
def get_user_performance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all performance records for current user
    """
    performances = db.query(Performance).filter(Performance.user_id == current_user.id).all()
    return performances

@router.get("/topic/{topic_id}", response_model=PerformanceResponse)
def get_topic_performance(topic_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get performance for a specific topic
    """
    performance = db.query(Performance).filter(
        Performance.user_id == current_user.id,
        Performance.topic_id == topic_id
    ).first()
    
    if not performance:
        # Return default if no record exists
        return PerformanceResponse(
            id=0,
            user_id=current_user.id,
            topic_id=topic_id,
            time_spent_minutes=0.0,
            last_accessed=None
        )
    
    return performance
