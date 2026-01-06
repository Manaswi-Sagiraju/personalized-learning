"""
SQLAlchemy database models
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class User(Base):
    """
    User model for authentication and profile management
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    performances = relationship("Performance", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")

class Course(Base):
    """
    Course model
    """
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    topics = relationship("Topic", back_populates="course", cascade="all, delete-orphan")

class Topic(Base):
    """
    Topic model with difficulty levels
    """
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    difficulty_level = Column(String, nullable=False)  # Beginner, Intermediate, Advanced
    order_index = Column(Integer, default=0)  # Order within course
    
    # Relationships
    course = relationship("Course", back_populates="topics")
    quizzes = relationship("Quiz", back_populates="topic", cascade="all, delete-orphan")
    performances = relationship("Performance", back_populates="topic")

class Quiz(Base):
    """
    Quiz model for topic assessments
    """
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String, nullable=False)
    questions = Column(Text, nullable=False)  # JSON string of questions
    answers = Column(Text, nullable=False)  # JSON string of correct answers
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    topic = relationship("Topic", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizAttempt(Base):
    """
    Quiz attempt model for tracking student quiz submissions
    """
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)  # Percentage score
    answers_submitted = Column(Text, nullable=False)  # JSON string
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")

class Performance(Base):
    """
    Performance tracking model for student learning analytics
    """
    __tablename__ = "performances"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    time_spent_minutes = Column(Float, default=0.0)
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="performances")
    topic = relationship("Topic", back_populates="performances")
