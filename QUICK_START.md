# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Initialize Database

```bash
python backend/init_data.py
```

You should see: `Sample data initialized successfully!`

## Step 3: Start the Backend Server

```bash
python run_server.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal window open!**

## Step 4: Start the Frontend Server

Open a **new terminal window** and run:

```bash
cd frontend
python -m http.server 8080
```

Or if you have Node.js:
```bash
cd frontend
npx http-server -p 8080
```

## Step 5: Access the Application

Open your browser and go to:
- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8000/docs

## Step 6: Create an Account

1. Click "Sign Up" tab
2. Fill in:
   - Username (e.g., "student1")
   - Email (e.g., "student1@example.com")
   - Password (e.g., "password123")
   - Full Name (optional)
3. Click "Sign Up"
4. You should see: "Account created successfully! Please login."

## Step 7: Login

1. Click "Login" tab
2. Enter your username and password
3. Click "Login"
4. You should be redirected to the Dashboard

## Troubleshooting

### If signup/login fails:

1. **Check server is running**: http://localhost:8000 should show API message
2. **Check browser console** (F12) for error messages
3. **Check server terminal** for backend errors
4. **Verify database exists**: `learning_platform.db` file should be present

### Common Issues:

- **"Cannot connect to server"**: Backend server not running
- **"Username already registered"**: Try a different username
- **"Incorrect username or password"**: Make sure you're using username (not email) to login

### Reset Everything:

1. Stop the server (Ctrl+C)
2. Delete `learning_platform.db`
3. Run `python backend/init_data.py` again
4. Restart the server

## Testing

Test authentication endpoints:
```bash
python test_auth.py
```

## Need Help?

See `TROUBLESHOOTING.md` for detailed troubleshooting steps.
