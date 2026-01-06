"""
Analytics and dashboard routes with visualizations
"""
import base64
import io
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from backend.database import get_db
from backend.models import User, Topic, QuizAttempt, Performance
from backend.schemas import DashboardData, ProgressData, TopicPerformanceData
from backend.auth import get_current_user

router = APIRouter()

@router.get("/dashboard", response_model=DashboardData)
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get comprehensive dashboard data for analytics
    """
    # Get all topics
    all_topics = db.query(Topic).all()
    total_topics = len(all_topics)
    
    # Get user's quiz attempts
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    
    # Calculate completed topics (topics with at least one attempt scoring >= 60)
    completed_topics = set()
    topic_scores = {}
    
    for attempt in attempts:
        quiz = attempt.quiz
        topic_id = quiz.topic_id
        
        if topic_id not in topic_scores:
            topic_scores[topic_id] = []
        topic_scores[topic_id].append(attempt.score)
        
        if attempt.score >= 60:
            completed_topics.add(topic_id)
    
    completed_count = len(completed_topics)
    completion_percentage = (completed_count / total_topics * 100) if total_topics > 0 else 0
    
    # Calculate average score
    all_scores = [attempt.score for attempt in attempts]
    average_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    # Progress over time (last 30 days)
    progress_data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    current_date = start_date
    cumulative_completed = 0
    
    while current_date <= end_date:
        # Count topics completed by this date
        completed_by_date = sum(
            1 for attempt in attempts
            if attempt.completed_at <= current_date and attempt.score >= 60
        )
        
        # Get average score up to this date
        scores_by_date = [
            attempt.score for attempt in attempts
            if attempt.completed_at <= current_date
        ]
        avg_score_by_date = sum(scores_by_date) / len(scores_by_date) if scores_by_date else 0
        
        progress_data.append(ProgressData(
            date=current_date.strftime("%Y-%m-%d"),
            topics_completed=completed_by_date,
            average_score=avg_score_by_date
        ))
        
        current_date += timedelta(days=1)
    
    # Topic-wise performance
    topic_performances = []
    for topic in all_topics:
        if topic.id in topic_scores:
            scores = topic_scores[topic.id]
            avg_score = sum(scores) / len(scores)
            attempts_count = len(scores)
            completion_status = "Completed" if avg_score >= 60 else "In Progress"
        else:
            avg_score = 0
            attempts_count = 0
            completion_status = "Not Started"
        
        topic_performances.append(TopicPerformanceData(
            topic_id=topic.id,
            topic_title=topic.title,
            average_score=avg_score,
            attempts_count=attempts_count,
            completion_status=completion_status
        ))
    
    return DashboardData(
        total_topics=total_topics,
        completed_topics=completed_count,
        completion_percentage=round(completion_percentage, 2),
        average_score=round(average_score, 2),
        progress_over_time=progress_data[-30:],  # Last 30 days
        topic_performances=topic_performances
    )

@router.get("/progress-chart")
def get_progress_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate progress chart image
    """
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    
    if not attempts:
        return {"error": "No data available"}
    
    # Prepare data
    dates = [attempt.completed_at.date() for attempt in attempts]
    scores = [attempt.score for attempt in attempts]
    
    # Create chart
    plt.figure(figsize=(10, 6))
    plt.plot(dates, scores, marker='o', linestyle='-', linewidth=2, markersize=4)
    plt.title('Quiz Scores Over Time', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Score (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Convert to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return {"image": f"data:image/png;base64,{img_base64}"}

@router.get("/topic-performance-chart")
def get_topic_performance_chart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Generate topic-wise performance chart
    """
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    
    if not attempts:
        return {"error": "No data available"}
    
    # Group by topic
    topic_scores = {}
    for attempt in attempts:
        quiz = attempt.quiz
        topic_title = quiz.topic.title
        if topic_title not in topic_scores:
            topic_scores[topic_title] = []
        topic_scores[topic_title].append(attempt.score)
    
    # Calculate averages
    topics = list(topic_scores.keys())
    avg_scores = [sum(scores) / len(scores) for scores in topic_scores.values()]
    
    # Create chart
    plt.figure(figsize=(12, 6))
    plt.barh(topics, avg_scores, color='steelblue', alpha=0.7)
    plt.title('Average Score by Topic', fontsize=16, fontweight='bold')
    plt.xlabel('Average Score (%)', fontsize=12)
    plt.ylabel('Topic', fontsize=12)
    plt.xlim(0, 100)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    
    # Convert to base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    plt.close()
    
    return {"image": f"data:image/png;base64,{img_base64}"}
