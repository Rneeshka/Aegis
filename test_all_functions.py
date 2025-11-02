#!/usr/bin/env python3
# test_all_functions.py
import requests
import json
import time

def test_all_functions():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование всех функций Aegis...")
    print(f"📍 URL: {base_url}")
    print("=" * 60)
    
    # Тест 1: Health check
    print("1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Password Recovery
    print("\n2. 🔐 Password Recovery")
    try:
        # Запрос кода восстановления
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Forgot password status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
        
        if "debug_code" in data:
            reset_code = data["debug_code"]
            print(f"   🔑 Reset code: {reset_code}")
            
            # Тест сброса пароля
            response = requests.post(f"{base_url}/auth/reset-password", 
                                    json={
                                        "email": "test@example.com",
                                        "code": reset_code,
                                        "new_password": "newpass123"
                                    }, 
                                    timeout=5)
            print(f"   ✅ Reset password status: {response.status_code}")
            print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API Key Validation (Expired)
    print("\n3. 🔑 API Key Validation (Expired)")
    try:
        # Создаем истекший ключ для тестирования
        expired_key = "PREMI-EXPIRED-TEST-KEY-12345"
        
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"},
                                headers={"X-API-Key": expired_key},
                                timeout=5)
        print(f"   ✅ Status with expired key: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Basic URL Check (без ключа)
    print("\n4. 🌐 Basic URL Check (без ключа)")
    try:
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 5: Admin UI
    print("\n5. 🎛️ Admin UI")
    try:
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
        if "API Keys" in response.text:
            print("   ✅ Admin UI содержит управление ключами")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 6: Account Registration
    print("\n6. 👤 Account Registration")
    try:
        response = requests.post(f"{base_url}/auth/register", 
                                json={
                                    "username": "testuser",
                                    "email": "testuser@example.com",
                                    "password": "testpass123",
                                    "api_key": "PREMI-12345-67890-ABCDE-FGHIJ-KLMNO"
                                }, 
                                timeout=5)
        print(f"   ✅ Registration status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_all_functions()
# test_all_functions.py
import requests
import json
import time

def test_all_functions():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование всех функций Aegis...")
    print(f"📍 URL: {base_url}")
    print("=" * 60)
    
    # Тест 1: Health check
    print("1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Password Recovery
    print("\n2. 🔐 Password Recovery")
    try:
        # Запрос кода восстановления
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Forgot password status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
        
        if "debug_code" in data:
            reset_code = data["debug_code"]
            print(f"   🔑 Reset code: {reset_code}")
            
            # Тест сброса пароля
            response = requests.post(f"{base_url}/auth/reset-password", 
                                    json={
                                        "email": "test@example.com",
                                        "code": reset_code,
                                        "new_password": "newpass123"
                                    }, 
                                    timeout=5)
            print(f"   ✅ Reset password status: {response.status_code}")
            print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API Key Validation (Expired)
    print("\n3. 🔑 API Key Validation (Expired)")
    try:
        # Создаем истекший ключ для тестирования
        expired_key = "PREMI-EXPIRED-TEST-KEY-12345"
        
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"},
                                headers={"X-API-Key": expired_key},
                                timeout=5)
        print(f"   ✅ Status with expired key: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Basic URL Check (без ключа)
    print("\n4. 🌐 Basic URL Check (без ключа)")
    try:
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 5: Admin UI
    print("\n5. 🎛️ Admin UI")
    try:
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
        if "API Keys" in response.text:
            print("   ✅ Admin UI содержит управление ключами")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 6: Account Registration
    print("\n6. 👤 Account Registration")
    try:
        response = requests.post(f"{base_url}/auth/register", 
                                json={
                                    "username": "testuser",
                                    "email": "testuser@example.com",
                                    "password": "testpass123",
                                    "api_key": "PREMI-12345-67890-ABCDE-FGHIJ-KLMNO"
                                }, 
                                timeout=5)
        print(f"   ✅ Registration status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_all_functions()
# test_all_functions.py
import requests
import json
import time

def test_all_functions():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование всех функций Aegis...")
    print(f"📍 URL: {base_url}")
    print("=" * 60)
    
    # Тест 1: Health check
    print("1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Password Recovery
    print("\n2. 🔐 Password Recovery")
    try:
        # Запрос кода восстановления
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Forgot password status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
        
        if "debug_code" in data:
            reset_code = data["debug_code"]
            print(f"   🔑 Reset code: {reset_code}")
            
            # Тест сброса пароля
            response = requests.post(f"{base_url}/auth/reset-password", 
                                    json={
                                        "email": "test@example.com",
                                        "code": reset_code,
                                        "new_password": "newpass123"
                                    }, 
                                    timeout=5)
            print(f"   ✅ Reset password status: {response.status_code}")
            print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API Key Validation (Expired)
    print("\n3. 🔑 API Key Validation (Expired)")
    try:
        # Создаем истекший ключ для тестирования
        expired_key = "PREMI-EXPIRED-TEST-KEY-12345"
        
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"},
                                headers={"X-API-Key": expired_key},
                                timeout=5)
        print(f"   ✅ Status with expired key: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Basic URL Check (без ключа)
    print("\n4. 🌐 Basic URL Check (без ключа)")
    try:
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 5: Admin UI
    print("\n5. 🎛️ Admin UI")
    try:
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
        if "API Keys" in response.text:
            print("   ✅ Admin UI содержит управление ключами")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 6: Account Registration
    print("\n6. 👤 Account Registration")
    try:
        response = requests.post(f"{base_url}/auth/register", 
                                json={
                                    "username": "testuser",
                                    "email": "testuser@example.com",
                                    "password": "testpass123",
                                    "api_key": "PREMI-12345-67890-ABCDE-FGHIJ-KLMNO"
                                }, 
                                timeout=5)
        print(f"   ✅ Registration status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_all_functions()
# test_all_functions.py
import requests
import json
import time

def test_all_functions():
    base_url = "http://127.0.0.1:8000"
    
    print("🔍 Тестирование всех функций Aegis...")
    print(f"📍 URL: {base_url}")
    print("=" * 60)
    
    # Тест 1: Health check
    print("1. 🏥 Health Check")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Тест 2: Password Recovery
    print("\n2. 🔐 Password Recovery")
    try:
        # Запрос кода восстановления
        response = requests.post(f"{base_url}/auth/forgot-password", 
                                json={"email": "test@example.com"}, 
                                timeout=5)
        print(f"   ✅ Forgot password status: {response.status_code}")
        data = response.json()
        print(f"   📄 Response: {data}")
        
        if "debug_code" in data:
            reset_code = data["debug_code"]
            print(f"   🔑 Reset code: {reset_code}")
            
            # Тест сброса пароля
            response = requests.post(f"{base_url}/auth/reset-password", 
                                    json={
                                        "email": "test@example.com",
                                        "code": reset_code,
                                        "new_password": "newpass123"
                                    }, 
                                    timeout=5)
            print(f"   ✅ Reset password status: {response.status_code}")
            print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 3: API Key Validation (Expired)
    print("\n3. 🔑 API Key Validation (Expired)")
    try:
        # Создаем истекший ключ для тестирования
        expired_key = "PREMI-EXPIRED-TEST-KEY-12345"
        
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"},
                                headers={"X-API-Key": expired_key},
                                timeout=5)
        print(f"   ✅ Status with expired key: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 4: Basic URL Check (без ключа)
    print("\n4. 🌐 Basic URL Check (без ключа)")
    try:
        response = requests.post(f"{base_url}/check/url", 
                                json={"url": "https://example.com"}, 
                                timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 5: Admin UI
    print("\n5. 🎛️ Admin UI")
    try:
        response = requests.get(f"{base_url}/admin/ui", timeout=5)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📄 Content length: {len(response.text)}")
        if "API Keys" in response.text:
            print("   ✅ Admin UI содержит управление ключами")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Тест 6: Account Registration
    print("\n6. 👤 Account Registration")
    try:
        response = requests.post(f"{base_url}/auth/register", 
                                json={
                                    "username": "testuser",
                                    "email": "testuser@example.com",
                                    "password": "testpass123",
                                    "api_key": "PREMI-12345-67890-ABCDE-FGHIJ-KLMNO"
                                }, 
                                timeout=5)
        print(f"   ✅ Registration status: {response.status_code}")
        print(f"   📄 Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Тестирование завершено!")
    return True

if __name__ == "__main__":
    test_all_functions()
