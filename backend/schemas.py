"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime

# Authentication schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    
    class Config:
        from_attributes = True

# Course schemas
class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None
    difficulty_level: str
    order_index: int = 0

class TopicCreate(TopicBase):
    course_id: int

class TopicResponse(TopicBase):
    id: int
    course_id: int
    
    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    topics: List[TopicResponse] = []
    
    class Config:
        from_attributes = True

# Quiz schemas
class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer_index: int

class QuizCreate(BaseModel):
    topic_id: int
    title: str
    questions: List[QuizQuestion]

class QuizResponse(BaseModel):
    id: int
    topic_id: int
    title: str
    questions: List[Dict[str, Any]]
    
    class Config:
        from_attributes = True

class QuizSubmission(BaseModel):
    quiz_id: int
    answers: List[int]  # List of selected answer indices

class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    score: float
    completed_at: datetime
    
    class Config:
        from_attributes = True

# Performance schemas
class PerformanceUpdate(BaseModel):
    topic_id: int
    time_spent_minutes: float

class PerformanceResponse(BaseModel):
    id: int
    user_id: int
    topic_id: int
    time_spent_minutes: float
    last_accessed: datetime
    
    class Config:
        from_attributes = True

# Recommendation schemas
class RecommendationResponse(BaseModel):
    topic_id: int
    topic_title: str
    difficulty_level: str
    recommendation_reason: str
    confidence_score: float

class KnowledgeGapResponse(BaseModel):
    topic_id: int
    topic_title: str
    difficulty_level: str
    is_weak: bool
    risk_score: float

# Analytics schemas
class ProgressData(BaseModel):
    date: str
    topics_completed: int
    average_score: float

class TopicPerformanceData(BaseModel):
    topic_id: int
    topic_title: str
    average_score: float
    attempts_count: int
    completion_status: str

class DashboardData(BaseModel):
    total_topics: int
    completed_topics: int
    completion_percentage: float
    average_score: float
    progress_over_time: List[ProgressData]
    topic_performances: List[TopicPerformanceData]
