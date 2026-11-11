import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
SIGN_IN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
SIGN_UP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"


def sign_in(email: str, password: str) -> dict:
    """Authenticate existing user via Firebase Auth REST API."""
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(SIGN_IN_URL, json=payload, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return {"success": True, "email": data["email"], "idToken": data["idToken"]}
        
        error_msg = data.get("error", {}).get("message", "Sign in failed.")
        return {"success": False, "error": error_msg}
    except Exception as exc:
        return {"success": False, "error": f"Connection error: {str(exc)}"}


def sign_up(email: str, password: str) -> dict:
    """Register a new user account via Firebase Auth REST API."""
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(SIGN_UP_URL, json=payload, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return {"success": True, "email": data["email"], "idToken": data["idToken"]}
        
        error_msg = data.get("error", {}).get("message", "Sign up failed.")
        return {"success": False, "error": error_msg}
    except Exception as exc:
        return {"success": False, "error": f"Connection error: {str(exc)}"}