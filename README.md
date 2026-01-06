# AI-Based Personalized Learning Platform

A complete personalized learning platform built with FastAPI (Python) backend and vanilla JavaScript frontend. Uses classical machine learning (Cosine Similarity, Logistic Regression) and rule-based logic for personalized recommendations.

## Features

- **User Authentication**: JWT-based secure authentication
- **Course Management**: Courses with multiple topics and difficulty levels
- **Quiz System**: Topic-wise quizzes with auto-evaluation
- **Performance Tracking**: Track scores, attempts, and time spent
- **Personalized Recommendations**: Content-based filtering using Cosine Similarity
- **Knowledge Gap Detection**: Logistic Regression for identifying weak areas
- **Adaptive Learning Path**: Rule-based adaptive recommendations
- **Analytics Dashboard**: Visual progress tracking with charts

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, Vanilla JavaScript
- **Database**: SQLite
- **Authentication**: JWT (JSON Web Tokens)
- **ML Libraries**: Pandas, NumPy, Scikit-learn
- **Visualization**: Matplotlib

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize database with sample data:
```bash
python backend/init_data.py
```

3. Start the FastAPI server (choose one method):

**Method 1: Using the run script**
```bash
python run_server.py
```

**Method 2: Using uvicorn directly**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

4. Open `frontend/index.html` in a web browser or serve it using a local server:

**Option A: Direct file access (may have CORS issues)**
- Simply open `frontend/index.html` in your browser

**Option B: Using Python HTTP server**
```bash
cd frontend
python -m http.server 8080
```

**Option C: Using Node.js http-server**
```bash
cd frontend
npx http-server -p 8080
```

5. Access the application:
- Frontend: http://localhost:8080 (if using server) or file:// path
- API Server: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Interactive API Docs: http://localhost:8000/redoc

## Usage

1. **Sign Up**: Create a new account
2. **Login**: Use your credentials to login
3. **Browse Courses**: View available courses and topics
4. **Take Quizzes**: Complete quizzes for each topic
5. **View Dashboard**: See your progress and analytics
6. **Get Recommendations**: View personalized topic recommendations
7. **Identify Knowledge Gaps**: See areas that need improvement

## API Endpoints

- `/api/auth/signup` - User registration
- `/api/auth/login` - User login
- `/api/auth/me` - Get current user info
- `/api/courses/` - Get all courses
- `/api/quizzes/submit` - Submit quiz answers
- `/api/performance/track` - Track learning time
- `/api/recommendations/topics` - Get topic recommendations
- `/api/recommendations/knowledge-gaps` - Detect knowledge gaps
- `/api/recommendations/adaptive-path` - Get adaptive learning path
- `/api/analytics/dashboard` - Get dashboard data

## Project Structure

```
personalized_learning_platform/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── init_data.py         # Initialize sample data
│   ├── routers/             # API routes
│   │   ├── auth.py
│   │   ├── courses.py
│   │   ├── quizzes.py
│   │   ├── performance.py
│   │   ├── recommendations.py
│   │   └── analytics.py
│   └── ml/                  # Machine learning modules
│       ├── recommendations.py    # Cosine Similarity
│       ├── knowledge_gaps.py     # Logistic Regression
│       └── adaptive_path.py      # Rule-based logic
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── styles.css           # Stylesheet
│   └── app.js               # JavaScript application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Notes

- The database file `learning_platform.db` will be created automatically
- Sample courses and topics are initialized via `init_data.py`
- JWT secret key should be changed in production (set via environment variable)
- CORS is enabled for all origins (restrict in production)
