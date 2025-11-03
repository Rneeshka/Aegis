@echo off
REM 🚀 Aegis - Автоматический запуск сервера (Windows)
REM Единый файл для запуска всего проекта

echo ============================================================
echo 🛡️  AEGIS - Антивирусное браузерное расширение
echo ============================================================
echo 🚀 Запуск сервера...
echo ============================================================

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден. Установите Python 3.8 или выше
    pause
    exit /b 1
)

REM Проверяем наличие папки antivirus-core
if not exist "antivirus-core" (
    echo ❌ Папка antivirus-core не найдена
    echo 💡 Запустите скрипт из корневой папки проекта
    pause
    exit /b 1
)

REM Переходим в папку antivirus-core
cd antivirus-core

REM Устанавливаем зависимости
echo 📦 Установка зависимостей...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Ошибка установки зависимостей
    pause
    exit /b 1
)

echo ✅ Зависимости установлены

REM Запускаем сервер
echo 🌐 Запуск сервера...
echo 📍 Адрес: http://127.0.0.1:9000
echo 📚 Документация: http://127.0.0.1:9000/docs
echo 🎛️  Admin UI: http://127.0.0.1:9000/admin/ui
echo 💚 Статус: http://127.0.0.1:9000/health
echo ============================================================
echo 🔄 Для остановки нажмите Ctrl+C
echo ============================================================

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --log-level info

echo.
echo 🛑 Сервер остановлен
pause

