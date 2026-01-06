"""
Initialize database with sample courses and topics
Run this script to populate initial data
"""
from backend.database import SessionLocal, engine, Base
from backend.models import Course, Topic, Quiz
import json

def init_data():
    """
    Create sample courses, topics, and quizzes
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Course).count() > 0:
            print("Data already initialized")
            return
        
        # Create Course 1: Python Programming
        course1 = Course(
            title="Python Programming",
            description="Learn Python from basics to advanced concepts"
        )
        db.add(course1)
        db.flush()
        
        # Topics for Python Course
        topics_python = [
            {"title": "Python Basics", "description": "Introduction to Python syntax and variables", "difficulty": "Beginner", "order": 1},
            {"title": "Data Structures", "description": "Lists, dictionaries, tuples, and sets", "difficulty": "Beginner", "order": 2},
            {"title": "Functions and Modules", "description": "Creating functions and organizing code", "difficulty": "Intermediate", "order": 3},
            {"title": "Object-Oriented Programming", "description": "Classes, objects, inheritance", "difficulty": "Intermediate", "order": 4},
            {"title": "Advanced Python", "description": "Decorators, generators, context managers", "difficulty": "Advanced", "order": 5},
        ]
        
        for topic_data in topics_python:
            topic = Topic(
                course_id=course1.id,
                title=topic_data["title"],
                description=topic_data["description"],
                difficulty_level=topic_data["difficulty"],
                order_index=topic_data["order"]
            )
            db.add(topic)
            db.flush()
            
            # Create sample quiz for each topic
            questions = [
                {
                    "question": f"Sample question 1 for {topic_data['title']}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer_index": 0
                },
                {
                    "question": f"Sample question 2 for {topic_data['title']}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer_index": 1
                },
                {
                    "question": f"Sample question 3 for {topic_data['title']}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer_index": 2
                }
            ]
            
            quiz = Quiz(
                topic_id=topic.id,
                title=f"Quiz: {topic_data['title']}",
                questions=json.dumps(questions),
                answers=json.dumps([0, 1, 2])
            )
            db.add(quiz)
        
        # Create Course 2: Machine Learning Fundamentals
        course2 = Course(
            title="Machine Learning Fundamentals",
            description="Introduction to ML concepts and algorithms"
        )
        db.add(course2)
        db.flush()
        
        # Topics for ML Course
        topics_ml = [
            {"title": "Introduction to ML", "description": "What is machine learning?", "difficulty": "Beginner", "order": 1},
            {"title": "Supervised Learning", "description": "Classification and regression", "difficulty": "Intermediate", "order": 2},
            {"title": "Unsupervised Learning", "description": "Clustering and dimensionality reduction", "difficulty": "Intermediate", "order": 3},
            {"title": "Neural Networks", "description": "Deep learning basics", "difficulty": "Advanced", "order": 4},
        ]
        
        for topic_data in topics_ml:
            topic = Topic(
                course_id=course2.id,
                title=topic_data["title"],
                description=topic_data["description"],
                difficulty_level=topic_data["difficulty"],
                order_index=topic_data["order"]
            )
            db.add(topic)
            db.flush()
            
            # Create sample quiz
            questions = [
                {
                    "question": f"ML question 1 for {topic_data['title']}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer_index": 0
                },
                {
                    "question": f"ML question 2 for {topic_data['title']}",
                    "options": ["Option A", "Option B", "Option C", "Option D"],
                    "correct_answer_index": 1
                }
            ]
            
            quiz = Quiz(
                topic_id=topic.id,
                title=f"Quiz: {topic_data['title']}",
                questions=json.dumps(questions),
                answers=json.dumps([0, 1])
            )
            db.add(quiz)
        
        db.commit()
        print("Sample data initialized successfully!")
        
    except Exception as e:
        db.rollback()
        print(f"Error initializing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_data()
