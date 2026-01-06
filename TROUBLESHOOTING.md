# Troubleshooting Guide

## Signup/Login Issues

### Issue: "Cannot connect to server" or "Network error"

**Solution:**
1. Make sure the FastAPI server is running:
   ```bash
   python run_server.py
   ```
   You should see: `INFO:     Uvicorn running on http://0.0.0.0:8000`

2. Verify the server is accessible:
   - Open http://localhost:8000 in your browser
   - You should see: `{"message":"AI-Based Personalized Learning Platform API"}`

3. Check if port 8000 is already in use:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

### Issue: "Username already registered" or "Email already registered"

**Solution:**
- The username/email is already taken. Try a different username or email.
- To reset the database, delete `learning_platform.db` and restart the server.

### Issue: "Incorrect username or password"

**Solution:**
1. Make sure you've signed up first
2. Check that you're using the correct username (not email) for login
3. Verify the password is correct

### Issue: Database errors

**Solution:**
1. Initialize the database:
   ```bash
   python backend/init_data.py
   ```

2. If you get import errors, make sure you're running from the project root:
   ```bash
   cd c:\Users\HP\Downloads\personalized_learning_platform
   python backend/init_data.py
   ```

3. Delete the database file and recreate:
   ```bash
   # Delete learning_platform.db
   python backend/init_data.py
   ```

### Issue: CORS errors in browser console

**Solution:**
- The CORS middleware is already configured in `backend/main.py`
- Make sure you're accessing the frontend through a web server, not file://
- Use: `python -m http.server 8080` in the frontend directory

### Issue: "Module not found" errors

**Solution:**
1. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you're running from the project root directory

3. Check Python path:
   ```bash
   python -c "import sys; print(sys.path)"
   ```

## Testing Authentication

Run the test script to verify authentication:
```bash
pip install requests  # If not already installed
python test_auth.py
```

## Common Fixes

1. **Restart the server** after making changes
2. **Clear browser cache** and localStorage
3. **Check browser console** (F12) for detailed error messages
4. **Check server logs** for backend errors

## Verification Steps

1. Server is running: http://localhost:8000
2. Database exists: `learning_platform.db` file should be present
3. Frontend can connect: Check browser console for API calls
4. API docs work: http://localhost:8000/docs
