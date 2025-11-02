# run_server.ps1
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🛡️  AEGIS - Антивирусное браузерное расширение" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔍 Поиск свободного порта..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

# Попробуем убить процесс на порту 8000
try {
    $processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($process in $processes) {
            $pid = $process.OwningProcess
            Write-Host "Убиваем процесс $pid на порту 8000" -ForegroundColor Red
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Host "Не удалось освободить порт 8000" -ForegroundColor Yellow
}

# Ждем немного
Start-Sleep -Seconds 2

# Запускаем сервер
Set-Location "antivirus-core"
Write-Host "🚀 Запуск сервера..." -ForegroundColor Green
Write-Host "📍 Адрес: http://127.0.0.1:8000" -ForegroundColor Blue
Write-Host "📚 Документация: http://127.0.0.1:8000/docs" -ForegroundColor Blue
Write-Host "🎛️  Admin UI: http://127.0.0.1:8000/admin/ui" -ForegroundColor Blue
Write-Host "💚 Статус: http://127.0.0.1:8000/health" -ForegroundColor Blue
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔄 Для остановки нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🛡️  AEGIS - Антивирусное браузерное расширение" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔍 Поиск свободного порта..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

# Попробуем убить процесс на порту 8000
try {
    $processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($process in $processes) {
            $pid = $process.OwningProcess
            Write-Host "Убиваем процесс $pid на порту 8000" -ForegroundColor Red
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Host "Не удалось освободить порт 8000" -ForegroundColor Yellow
}

# Ждем немного
Start-Sleep -Seconds 2

# Запускаем сервер
Set-Location "antivirus-core"
Write-Host "🚀 Запуск сервера..." -ForegroundColor Green
Write-Host "📍 Адрес: http://127.0.0.1:8000" -ForegroundColor Blue
Write-Host "📚 Документация: http://127.0.0.1:8000/docs" -ForegroundColor Blue
Write-Host "🎛️  Admin UI: http://127.0.0.1:8000/admin/ui" -ForegroundColor Blue
Write-Host "💚 Статус: http://127.0.0.1:8000/health" -ForegroundColor Blue
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔄 Для остановки нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🛡️  AEGIS - Антивирусное браузерное расширение" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔍 Поиск свободного порта..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

# Попробуем убить процесс на порту 8000
try {
    $processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($process in $processes) {
            $pid = $process.OwningProcess
            Write-Host "Убиваем процесс $pid на порту 8000" -ForegroundColor Red
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Host "Не удалось освободить порт 8000" -ForegroundColor Yellow
}

# Ждем немного
Start-Sleep -Seconds 2

# Запускаем сервер
Set-Location "antivirus-core"
Write-Host "🚀 Запуск сервера..." -ForegroundColor Green
Write-Host "📍 Адрес: http://127.0.0.1:8000" -ForegroundColor Blue
Write-Host "📚 Документация: http://127.0.0.1:8000/docs" -ForegroundColor Blue
Write-Host "🎛️  Admin UI: http://127.0.0.1:8000/admin/ui" -ForegroundColor Blue
Write-Host "💚 Статус: http://127.0.0.1:8000/health" -ForegroundColor Blue
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔄 Для остановки нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🛡️  AEGIS - Антивирусное браузерное расширение" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔍 Поиск свободного порта..." -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

# Попробуем убить процесс на порту 8000
try {
    $processes = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
    if ($processes) {
        foreach ($process in $processes) {
            $pid = $process.OwningProcess
            Write-Host "Убиваем процесс $pid на порту 8000" -ForegroundColor Red
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
        }
    }
} catch {
    Write-Host "Не удалось освободить порт 8000" -ForegroundColor Yellow
}

# Ждем немного
Start-Sleep -Seconds 2

# Запускаем сервер
Set-Location "antivirus-core"
Write-Host "🚀 Запуск сервера..." -ForegroundColor Green
Write-Host "📍 Адрес: http://127.0.0.1:8000" -ForegroundColor Blue
Write-Host "📚 Документация: http://127.0.0.1:8000/docs" -ForegroundColor Blue
Write-Host "🎛️  Admin UI: http://127.0.0.1:8000/admin/ui" -ForegroundColor Blue
Write-Host "💚 Статус: http://127.0.0.1:8000/health" -ForegroundColor Blue
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🔄 Для остановки нажмите Ctrl+C" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan

python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
