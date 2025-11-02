#!/usr/bin/env python3
# test_server.py
import requests
import json

def test_server():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование сервера...")
    print(f"📍 URL: {base_url}")
    print("=" * 50)
    
    # Тест 1: Health check
    try:
        print("1. Тест /health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Admin UI
    try:
        print("\n2. Тест /admin/ui...")
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API endpoints
    try:
        print("\n3. Тест /check/url...")
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Password recovery
    try:
        print("\n4. Тест /auth/forgot-password...")
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_server()
# test_server.py
import requests
import json

def test_server():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование сервера...")
    print(f"📍 URL: {base_url}")
    print("=" * 50)
    
    # Тест 1: Health check
    try:
        print("1. Тест /health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Admin UI
    try:
        print("\n2. Тест /admin/ui...")
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API endpoints
    try:
        print("\n3. Тест /check/url...")
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Password recovery
    try:
        print("\n4. Тест /auth/forgot-password...")
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_server()
# test_server.py
import requests
import json

def test_server():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование сервера...")
    print(f"📍 URL: {base_url}")
    print("=" * 50)
    
    # Тест 1: Health check
    try:
        print("1. Тест /health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Admin UI
    try:
        print("\n2. Тест /admin/ui...")
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API endpoints
    try:
        print("\n3. Тест /check/url...")
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Password recovery
    try:
        print("\n4. Тест /auth/forgot-password...")
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_server()
# test_server.py
import requests
import json

def test_server():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование сервера...")
    print(f"📍 URL: {base_url}")
    print("=" * 50)
    
    # Тест 1: Health check
    try:
        print("1. Тест /health...")
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Admin UI
    try:
        print("\n2. Тест /admin/ui...")
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API endpoints
    try:
        print("\n3. Тест /check/url...")
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Password recovery
    try:
        print("\n4. Тест /auth/forgot-password...")
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_server()
