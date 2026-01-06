"""
Quiz and assessment routes
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models import Quiz, QuizAttempt, User, Topic
from backend.schemas import QuizCreate, QuizResponse, QuizSubmission, QuizAttemptResponse
from backend.auth import get_current_user

router = APIRouter()

@router.get("/topic/{topic_id}", response_model=List[QuizResponse])
def get_quizzes_by_topic(topic_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all quizzes for a specific topic
    """
    quizzes = db.query(Quiz).filter(Quiz.topic_id == topic_id).all()
    return quizzes

@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(quiz_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get a specific quiz by ID (without answers)
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Parse questions and remove correct answers for security
    questions_data = json.loads(quiz.questions)
    questions_without_answers = []
    for q in questions_data:
        questions_without_answers.append({
            "question": q["question"],
            "options": q["options"]
        })
    
    quiz_dict = {
        "id": quiz.id,
        "topic_id": quiz.topic_id,
        "title": quiz.title,
        "questions": questions_without_answers
    }
    return quiz_dict

@router.post("/", response_model=QuizResponse)
def create_quiz(quiz_data: QuizCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new quiz
    """
    # Verify topic exists
    topic = db.query(Topic).filter(Topic.id == quiz_data.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    # Prepare questions and answers
    questions_list = []
    answers_list = []
    for q in quiz_data.questions:
        questions_list.append({
            "question": q.question,
            "options": q.options,
            "correct_answer_index": q.correct_answer_index
        })
        answers_list.append(q.correct_answer_index)
    
    db_quiz = Quiz(
        topic_id=quiz_data.topic_id,
        title=quiz_data.title,
        questions=json.dumps(questions_list),
        answers=json.dumps(answers_list)
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    
    # Return quiz without answers
    questions_without_answers = []
    for q in questions_list:
        questions_without_answers.append({
            "question": q["question"],
            "options": q["options"]
        })
    
    return {
        "id": db_quiz.id,
        "topic_id": db_quiz.topic_id,
        "title": db_quiz.title,
        "questions": questions_without_answers
    }

@router.post("/submit", response_model=QuizAttemptResponse)
def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Submit quiz answers and get score
    """
    quiz = db.query(Quiz).filter(Quiz.id == submission.quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Parse correct answers
    correct_answers = json.loads(quiz.answers)
    
    # Calculate score
    correct_count = 0
    for i, answer in enumerate(submission.answers):
        if i < len(correct_answers) and answer == correct_answers[i]:
            correct_count += 1
    
    score = (correct_count / len(correct_answers)) * 100 if correct_answers else 0
    
    # Save attempt
    db_attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=submission.quiz_id,
        score=score,
        answers_submitted=json.dumps(submission.answers)
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)
    
    return db_attempt

@router.get("/attempts/user", response_model=List[QuizAttemptResponse])
def get_user_attempts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get all quiz attempts for current user
    """
    attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    return attempts
