// API Configuration
const API_BASE_URL = 'http://localhost:8000/api';

// Token management
let authToken = localStorage.getItem('authToken');

// API helper functions
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }
    
    try {
        const response = await fetch(url, {
            ...options,
            headers
        });
        
        if (response.status === 401) {
            // Unauthorized - redirect to login
            logout();
            return { error: 'Unauthorized' };
        }
        
        // Try to parse JSON response
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            return { error: text || 'Unknown error' };
        }
        
        // Check if response indicates an error
        if (!response.ok) {
            return { error: data.detail || data.message || 'Request failed' };
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            return { error: 'Cannot connect to server. Make sure the backend server is running on http://localhost:8000' };
        }
        return { error: error.message || 'Network error. Make sure the server is running.' };
    }
}

// Authentication functions
function switchAuthTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(form => form.classList.remove('active'));
    
    if (tab === 'login') {
        document.querySelector('.tab-btn').classList.add('active');
        document.getElementById('login-form').classList.add('active');
    } else {
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('signup-form').classList.add('active');
    }
}

async function handleLogin() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');
    const loadingDiv = document.getElementById('login-loading');
    const loginBtn = document.getElementById('login-btn');
    
    if (!username || !password) {
        errorDiv.textContent = 'Please fill in all fields';
        errorDiv.classList.add('show');
        return;
    }
    
    // Clear previous errors and show loading
    errorDiv.classList.remove('show');
    errorDiv.textContent = '';
    loadingDiv.style.display = 'block';
    loginBtn.disabled = true;
    loginBtn.textContent = 'Logging in...';
    
    try {
        const response = await apiCall('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ username, password })
        });
        
        loadingDiv.style.display = 'none';
        loginBtn.disabled = false;
        loginBtn.textContent = 'Login';
        
        if (response && response.error) {
            errorDiv.textContent = response.error;
            errorDiv.classList.add('show');
            return;
        }
        
        if (response && response.access_token) {
            authToken = response.access_token;
            localStorage.setItem('authToken', authToken);
            errorDiv.classList.remove('show');
            showPage('dashboard');
            loadDashboard();
        } else {
            errorDiv.textContent = response?.error || 'Invalid username or password';
            errorDiv.classList.add('show');
        }
    } catch (error) {
        loadingDiv.style.display = 'none';
        loginBtn.disabled = false;
        loginBtn.textContent = 'Login';
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.classList.add('show');
    }
}

async function handleSignup() {
    const username = document.getElementById('signup-username').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const fullName = document.getElementById('signup-fullname').value;
    const errorDiv = document.getElementById('signup-error');
    const loadingDiv = document.getElementById('signup-loading');
    const signupBtn = document.getElementById('signup-btn');
    
    if (!username || !email || !password) {
        errorDiv.textContent = 'Please fill in all required fields';
        errorDiv.classList.add('show');
        return;
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errorDiv.textContent = 'Please enter a valid email address';
        errorDiv.classList.add('show');
        return;
    }
    
    // Clear previous errors and show loading
    errorDiv.classList.remove('show');
    errorDiv.textContent = '';
    loadingDiv.style.display = 'block';
    signupBtn.disabled = true;
    signupBtn.textContent = 'Creating account...';
    
    try {
        const response = await apiCall('/auth/signup', {
            method: 'POST',
            body: JSON.stringify({ username, email, password, full_name: fullName })
        });
        
        loadingDiv.style.display = 'none';
        signupBtn.disabled = false;
        signupBtn.textContent = 'Sign Up';
        
        if (response && response.error) {
            errorDiv.textContent = response.error;
            errorDiv.classList.add('show');
            return;
        }
        
        if (response && response.id) {
            errorDiv.classList.remove('show');
            alert('Account created successfully! Please login.');
            // Clear form
            document.getElementById('signup-username').value = '';
            document.getElementById('signup-email').value = '';
            document.getElementById('signup-password').value = '';
            document.getElementById('signup-fullname').value = '';
            switchAuthTab('login');
        } else {
            errorDiv.textContent = response?.error || response?.detail || 'Signup failed. Please try again.';
            errorDiv.classList.add('show');
        }
    } catch (error) {
        loadingDiv.style.display = 'none';
        signupBtn.disabled = false;
        signupBtn.textContent = 'Sign Up';
        errorDiv.textContent = 'An error occurred. Please try again.';
        errorDiv.classList.add('show');
    }
}

function logout() {
    authToken = null;
    localStorage.removeItem('authToken');
    showPage('login');
    document.getElementById('login-username').value = '';
    document.getElementById('login-password').value = '';
}

// Page navigation
function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    document.getElementById(`${pageId}-page`).classList.add('active');
    
    // Load page-specific data
    if (pageId === 'dashboard' && authToken) {
        loadDashboard();
    } else if (pageId === 'courses' && authToken) {
        loadCourses();
    } else if (pageId === 'recommendations' && authToken) {
        loadRecommendations();
    }
}

// Dashboard functions
async function loadDashboard() {
    const dashboardData = await apiCall('/analytics/dashboard');
    
    if (!dashboardData) return;
    
    document.getElementById('completion-rate').textContent = `${dashboardData.completion_percentage}%`;
    document.getElementById('average-score').textContent = `${dashboardData.average_score}%`;
    document.getElementById('topics-completed').textContent = dashboardData.completed_topics;
    document.getElementById('total-topics').textContent = dashboardData.total_topics;
    
    // Load charts
    loadProgressChart();
    loadTopicPerformanceChart();
}

async function loadProgressChart() {
    const chartData = await apiCall('/analytics/progress-chart');
    if (chartData && chartData.image) {
        document.getElementById('progress-chart').innerHTML = `<img src="${chartData.image}" alt="Progress Chart">`;
    }
}

async function loadTopicPerformanceChart() {
    const chartData = await apiCall('/analytics/topic-performance-chart');
    if (chartData && chartData.image) {
        document.getElementById('topic-performance-chart').innerHTML = `<img src="${chartData.image}" alt="Topic Performance Chart">`;
    }
}

// Courses functions
async function loadCourses() {
    const courses = await apiCall('/courses/');
    
    if (!courses) return;
    
    const coursesList = document.getElementById('courses-list');
    coursesList.innerHTML = '';
    
    courses.forEach(course => {
        const courseCard = document.createElement('div');
        courseCard.className = 'course-card';
        courseCard.innerHTML = `
            <h3>${course.title}</h3>
            <p>${course.description || ''}</p>
            <div class="topic-list">
                ${course.topics.map(topic => `
                    <div class="topic-item" onclick="loadTopic(${topic.id})">
                        <h4>${topic.title}</h4>
                        <p>${topic.description || ''}</p>
                        <span class="difficulty-badge ${topic.difficulty_level.toLowerCase()}">${topic.difficulty_level}</span>
                    </div>
                `).join('')}
            </div>
        `;
        coursesList.appendChild(courseCard);
    });
}

async function loadTopic(topicId) {
    const topic = await apiCall(`/courses/topics/${topicId}`);
    
    if (!topic) return;
    
    showPage('topic-detail');
    const topicDetail = document.getElementById('topic-detail');
    topicDetail.innerHTML = `
        <h2>${topic.title}</h2>
        <p>${topic.description || ''}</p>
        <p><strong>Difficulty:</strong> <span class="difficulty-badge ${topic.difficulty_level.toLowerCase()}">${topic.difficulty_level}</span></p>
        <button onclick="startQuiz(${topicId})" class="submit-btn" style="margin-top: 1rem;">Take Quiz</button>
    `;
}

async function startQuiz(topicId) {
    const quizzes = await apiCall(`/quizzes/topic/${topicId}`);
    
    if (!quizzes || quizzes.length === 0) {
        alert('No quiz available for this topic');
        return;
    }
    
    const quiz = await apiCall(`/quizzes/${quizzes[0].id}`);
    
    if (!quiz) return;
    
    showPage('quiz-page');
    document.getElementById('quiz-title').textContent = quiz.title;
    
    const quizQuestions = document.getElementById('quiz-questions');
    quizQuestions.innerHTML = '';
    
    quiz.questions.forEach((question, qIndex) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'quiz-question';
        questionDiv.innerHTML = `
            <h4>${qIndex + 1}. ${question.question}</h4>
            ${question.options.map((option, oIndex) => `
                <div class="quiz-option" onclick="selectOption(${qIndex}, ${oIndex})" id="q${qIndex}_o${oIndex}">
                    ${option}
                </div>
            `).join('')}
        `;
        quizQuestions.appendChild(questionDiv);
    });
    
    window.currentQuiz = { id: quiz.id, questions: quiz.questions, answers: [] };
}

function selectOption(questionIndex, optionIndex) {
    if (!window.currentQuiz) return;
    
    // Remove previous selection
    const questionDiv = document.querySelector(`#quiz-questions > div:nth-child(${questionIndex + 1})`);
    questionDiv.querySelectorAll('.quiz-option').forEach(opt => opt.classList.remove('selected'));
    
    // Add new selection
    document.getElementById(`q${questionIndex}_o${optionIndex}`).classList.add('selected');
    window.currentQuiz.answers[questionIndex] = optionIndex;
}

async function submitQuiz() {
    if (!window.currentQuiz) return;
    
    const submission = {
        quiz_id: window.currentQuiz.id,
        answers: window.currentQuiz.questions.map((_, index) => window.currentQuiz.answers[index] || 0)
    };
    
    const result = await apiCall('/quizzes/submit', {
        method: 'POST',
        body: JSON.stringify(submission)
    });
    
    if (result) {
        const quizResult = document.getElementById('quiz-result');
        quizResult.innerHTML = `
            <h3>Quiz Completed!</h3>
            <p>Your Score: <strong>${result.score.toFixed(1)}%</strong></p>
            <button onclick="showPage('courses')" class="submit-btn">Back to Courses</button>
        `;
    }
}

// Recommendations functions
async function loadRecommendations() {
    // Load topic recommendations
    const topicRecs = await apiCall('/recommendations/topics?limit=5');
    if (topicRecs) {
        const container = document.getElementById('topic-recommendations');
        container.innerHTML = topicRecs.map(rec => `
            <div class="recommendation-card">
                <h4>${rec.topic_title}</h4>
                <p><strong>Difficulty:</strong> <span class="difficulty-badge ${rec.difficulty_level.toLowerCase()}">${rec.difficulty_level}</span></p>
                <p>${rec.recommendation_reason}</p>
                <span class="confidence-score">Confidence: ${(rec.confidence_score * 100).toFixed(1)}%</span>
            </div>
        `).join('');
    }
    
    // Load knowledge gaps
    const gaps = await apiCall('/recommendations/knowledge-gaps');
    if (gaps) {
        const container = document.getElementById('knowledge-gaps');
        container.innerHTML = gaps.slice(0, 5).map(gap => `
            <div class="recommendation-card">
                <h4>${gap.topic_title}</h4>
                <p><strong>Status:</strong> <span class="risk-badge ${gap.is_weak ? 'high' : 'low'}">${gap.is_weak ? 'Weak Area' : 'Strong'}</span></p>
                <p><strong>Risk Score:</strong> ${(gap.risk_score * 100).toFixed(1)}%</p>
            </div>
        `).join('');
    }
    
    // Load adaptive path
    const adaptivePath = await apiCall('/recommendations/adaptive-path');
    if (adaptivePath) {
        const container = document.getElementById('adaptive-path');
        container.innerHTML = adaptivePath.map(rec => `
            <div class="recommendation-card">
                <h4>${rec.topic_title}</h4>
                <p><strong>Difficulty:</strong> <span class="difficulty-badge ${rec.difficulty_level.toLowerCase()}">${rec.difficulty_level}</span></p>
                <p>${rec.recommendation_reason}</p>
            </div>
        `).join('');
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    if (authToken) {
        showPage('dashboard');
        loadDashboard();
    } else {
        showPage('login');
    }
});
