#!/usr/bin/env python3
"""
🚀 Aegis - Автоматический запуск сервера
Единый файл для запуска всего проекта
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Красивый баннер при запуске"""
    print("=" * 60)
    print("🛡️  AEGIS - Антивирусное браузерное расширение")
    print("=" * 60)
    print("🚀 Запуск сервера...")
    print("=" * 60)

def check_requirements():
    """Проверка зависимостей"""
    print("📋 Проверка зависимостей...")
    
    # Проверяем Python версию
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        return False
    
    # Проверяем наличие requirements.txt
    req_file = Path("antivirus-core/requirements.txt")
    if not req_file.exists():
        print("❌ Файл requirements.txt не найден")
        return False
    
    print("✅ Зависимости проверены")
    return True

def install_dependencies():
    """Установка зависимостей"""
    print("📦 Установка зависимостей...")
    
    try:
        # Переходим в папку antivirus-core
        os.chdir("antivirus-core")
        
        # Устанавливаем зависимости
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Зависимости установлены")
            return True
        else:
            print(f"❌ Ошибка установки: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def start_server():
    """Запуск сервера"""
    print("🌐 Запуск сервера...")
    print("📍 Адрес: http://127.0.0.1:8000")
    print("📚 Документация: http://127.0.0.1:8000/docs")
    print("🎛️  Admin UI: http://127.0.0.1:8000/admin/ui")
    print("💚 Статус: http://127.0.0.1:8000/health")
    print("=" * 60)
    print("🔄 Для остановки нажмите Ctrl+C")
    print("=" * 60)
    
    try:
        # Запускаем uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен")
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")

def main():
    """Главная функция"""
    print_banner()
    
    # Проверяем, что мы в правильной папке
    if not Path("antivirus-core").exists():
        print("❌ Папка antivirus-core не найдена")
        print("💡 Запустите скрипт из корневой папки проекта")
        return
    
    # Проверяем зависимости
    if not check_requirements():
        return
    
    # Устанавливаем зависимости
    if not install_dependencies():
        return
    
    # Запускаем сервер
    start_server()

if __name__ == "__main__":
    main()

