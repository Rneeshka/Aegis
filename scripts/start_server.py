#!/usr/bin/env python3
"""
Скрипт для запуска Aegis Backend сервера
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Запуск сервера с правильными путями"""
    
    # Определяем корневую папку проекта
    project_root = Path(__file__).parent.parent
    backend_dir = project_root / "backend"
    
    # Проверяем существование backend папки
    if not backend_dir.exists():
        print("❌ Ошибка: папка backend не найдена!")
        print(f"Ожидаемый путь: {backend_dir}")
        return 1
    
    # Переходим в папку backend
    os.chdir(backend_dir)
    
    print("🚀 Запуск Aegis Backend сервера...")
    print(f"📁 Рабочая папка: {backend_dir}")
    print("🌐 Сервер будет доступен по адресу: http://127.0.0.1:8000")
    print("📚 API документация: http://127.0.0.1:8000/docs")
    print("🛠️ Admin UI: http://127.0.0.1:8000/admin/ui")
    print("=" * 50)
    
    try:
        # Запускаем сервер
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска сервера: {e}")
        return 1
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())





