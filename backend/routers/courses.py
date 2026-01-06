"""
Course and topic management routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Course, Topic, User
from backend.schemas import CourseCreate, CourseResponse, TopicCreate, TopicResponse
from backend.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all courses with their topics
    """
    courses = db.query(Course).all()
    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get a specific course by ID
    """
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/", response_model=CourseResponse)
def create_course(course_data: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new course
    """
    db_course = Course(
        title=course_data.title,
        description=course_data.description
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@router.get("/topics/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get a specific topic by ID
    """
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic

@router.post("/topics", response_model=TopicResponse)
def create_topic(topic_data: TopicCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new topic
    """
    # Verify course exists
    course = db.query(Course).filter(Course.id == topic_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_topic = Topic(
        course_id=topic_data.course_id,
        title=topic_data.title,
        description=topic_data.description,
        difficulty_level=topic_data.difficulty_level,
        order_index=topic_data.order_index
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic
