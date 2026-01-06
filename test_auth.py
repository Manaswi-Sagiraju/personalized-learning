"""
Simple test script to verify authentication endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth"

def test_signup():
    """Test user signup"""
    print("Testing signup...")
    signup_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/signup", json=signup_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Make sure the server is running!")
        print("Run: python run_server.py")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_login():
    """Test user login"""
    print("\nTesting login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/login", json=login_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Make sure the server is running!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Authentication Test Script")
    print("=" * 50)
    
    # Test signup
    signup_success = test_signup()
    
    # Test login
    login_success = test_login()
    
    print("\n" + "=" * 50)
    if signup_success and login_success:
        print("All tests passed!")
    else:
        print("Some tests failed. Check the errors above.")
    print("=" * 50)
