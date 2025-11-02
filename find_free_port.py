#!/usr/bin/env python3
# find_free_port.py
import socket
import subprocess
import sys
import os

def find_free_port(start_port=8000, max_port=8010):
    """Находит свободный порт начиная с start_port"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

def kill_process_on_port(port):
    """Убивает процесс на указанном порту"""
    try:
        # Для Windows используем netstat и taskkill
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print(f"Killing process {pid} on port {port}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    return True
    except Exception as e:
        print(f"Error killing process: {e}")
    return False

def main():
    print("🔍 Поиск свободного порта...")
    
    # Сначала попробуем освободить порт 8000
    if kill_process_on_port(8000):
        print("✅ Освободили порт 8000")
        port = 8000
    else:
        # Ищем свободный порт
        port = find_free_port()
        if not port:
            print("❌ Не удалось найти свободный порт")
            return
    
    print(f"🚀 Запуск сервера на порту {port}")
    print(f"📍 Адрес: http://127.0.0.1:{port}")
    print(f"📚 Документация: http://127.0.0.1:{port}/docs")
    print(f"🎛️ Admin UI: http://127.0.0.1:{port}/admin/ui")
    print(f"💚 Статус: http://127.0.0.1:{port}/health")
    print("=" * 60)
    
    try:
        # Запускаем сервер
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '127.0.0.1', 
            '--port', str(port),
            '--reload'
        ], cwd='antivirus-core')
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
# find_free_port.py
import socket
import subprocess
import sys
import os

def find_free_port(start_port=8000, max_port=8010):
    """Находит свободный порт начиная с start_port"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

def kill_process_on_port(port):
    """Убивает процесс на указанном порту"""
    try:
        # Для Windows используем netstat и taskkill
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print(f"Killing process {pid} on port {port}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    return True
    except Exception as e:
        print(f"Error killing process: {e}")
    return False

def main():
    print("🔍 Поиск свободного порта...")
    
    # Сначала попробуем освободить порт 8000
    if kill_process_on_port(8000):
        print("✅ Освободили порт 8000")
        port = 8000
    else:
        # Ищем свободный порт
        port = find_free_port()
        if not port:
            print("❌ Не удалось найти свободный порт")
            return
    
    print(f"🚀 Запуск сервера на порту {port}")
    print(f"📍 Адрес: http://127.0.0.1:{port}")
    print(f"📚 Документация: http://127.0.0.1:{port}/docs")
    print(f"🎛️ Admin UI: http://127.0.0.1:{port}/admin/ui")
    print(f"💚 Статус: http://127.0.0.1:{port}/health")
    print("=" * 60)
    
    try:
        # Запускаем сервер
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '127.0.0.1', 
            '--port', str(port),
            '--reload'
        ], cwd='antivirus-core')
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
# find_free_port.py
import socket
import subprocess
import sys
import os

def find_free_port(start_port=8000, max_port=8010):
    """Находит свободный порт начиная с start_port"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

def kill_process_on_port(port):
    """Убивает процесс на указанном порту"""
    try:
        # Для Windows используем netstat и taskkill
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print(f"Killing process {pid} on port {port}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    return True
    except Exception as e:
        print(f"Error killing process: {e}")
    return False

def main():
    print("🔍 Поиск свободного порта...")
    
    # Сначала попробуем освободить порт 8000
    if kill_process_on_port(8000):
        print("✅ Освободили порт 8000")
        port = 8000
    else:
        # Ищем свободный порт
        port = find_free_port()
        if not port:
            print("❌ Не удалось найти свободный порт")
            return
    
    print(f"🚀 Запуск сервера на порту {port}")
    print(f"📍 Адрес: http://127.0.0.1:{port}")
    print(f"📚 Документация: http://127.0.0.1:{port}/docs")
    print(f"🎛️ Admin UI: http://127.0.0.1:{port}/admin/ui")
    print(f"💚 Статус: http://127.0.0.1:{port}/health")
    print("=" * 60)
    
    try:
        # Запускаем сервер
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '127.0.0.1', 
            '--port', str(port),
            '--reload'
        ], cwd='antivirus-core')
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
# find_free_port.py
import socket
import subprocess
import sys
import os

def find_free_port(start_port=8000, max_port=8010):
    """Находит свободный порт начиная с start_port"""
    for port in range(start_port, max_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('127.0.0.1', port))
                return port
        except OSError:
            continue
    return None

def kill_process_on_port(port):
    """Убивает процесс на указанном порту"""
    try:
        # Для Windows используем netstat и taskkill
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print(f"Killing process {pid} on port {port}")
                    subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
                    return True
    except Exception as e:
        print(f"Error killing process: {e}")
    return False

def main():
    print("🔍 Поиск свободного порта...")
    
    # Сначала попробуем освободить порт 8000
    if kill_process_on_port(8000):
        print("✅ Освободили порт 8000")
        port = 8000
    else:
        # Ищем свободный порт
        port = find_free_port()
        if not port:
            print("❌ Не удалось найти свободный порт")
            return
    
    print(f"🚀 Запуск сервера на порту {port}")
    print(f"📍 Адрес: http://127.0.0.1:{port}")
    print(f"📚 Документация: http://127.0.0.1:{port}/docs")
    print(f"🎛️ Admin UI: http://127.0.0.1:{port}/admin/ui")
    print(f"💚 Статус: http://127.0.0.1:{port}/health")
    print("=" * 60)
    
    try:
        # Запускаем сервер
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '127.0.0.1', 
            '--port', str(port),
            '--reload'
        ], cwd='antivirus-core')
        
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
