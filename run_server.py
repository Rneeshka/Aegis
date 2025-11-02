#!/usr/bin/env python3
# run_server.py
import sys
import os
import subprocess

# Добавляем путь к модулю
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'antivirus-core'))

def run_server():
    try:
        print("🚀 Starting Aegis server...")
        print("📍 Address: http://127.0.0.1:8000")
        print("📚 Documentation: http://127.0.0.1:8000/docs")
        print("🎛️ Admin UI: http://127.0.0.1:8000/admin/ui")
        print("💚 Status: http://127.0.0.1:8000/health")
        print("=" * 60)
        
        # Запускаем сервер
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '127.0.0.1', 
            '--port', '8000',
            '--reload'
        ], cwd='antivirus-core')
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_server()
