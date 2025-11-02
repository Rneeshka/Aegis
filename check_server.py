#!/usr/bin/env python3
# check_server.py
import requests
import time

def check_server():
    try:
        response = requests.get('http://127.0.0.1:8000/health', timeout=5)
        print(f"✅ Server is running! Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("Checking server status...")
    check_server()
