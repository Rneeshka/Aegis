# quick_test.ps1
# Быстрый тест всех функций API

param(
    [string]$BaseUrl = "http://127.0.0.1:8000",
    [string]$PremiumApiKey = "PREMI-12345-67890-ABCDE-FGHIJ-KLMNO"
)

Write-Host "🧪 Быстрый тест Antivirus Core API" -ForegroundColor Cyan
Write-Host "Base URL: $BaseUrl" -ForegroundColor Gray
Write-Host ""

# Функция для выполнения HTTP запросов
function Invoke-TestRequest {
    param(
        [string]$Method,
        [string]$Endpoint,
        [hashtable]$Headers = @{},
        [string]$Body = $null,
        [string]$ApiKey = $null,
        [string]$TestName
    )
    
    $url = "$BaseUrl$Endpoint"
    if ($ApiKey) {
        $headers["X-API-Key"] = $ApiKey
    }
    
    Write-Host "  Тестируем: $TestName" -ForegroundColor Yellow
    
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $url -Method $Method -Headers $Headers -Body $Body -ContentType "application/json"
        } else {
            $response = Invoke-RestMethod -Uri $url -Method $Method -Headers $Headers
        }
        Write-Host "  ✅ Успешно" -ForegroundColor Green
        return $response
    } catch {
        Write-Host "  ❌ Ошибка: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

Write-Host "1. 🔍 Проверка состояния системы..." -ForegroundColor Cyan
$health = Invoke-TestRequest -Method "GET" -Endpoint "/health" -TestName "Health Check"
if ($health) {
    Write-Host "   База данных: $($health.database)" -ForegroundColor Gray
    Write-Host "   Внешние API: $($health.external_apis | ConvertTo-Json -Compress)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "2. 🌐 Базовые функции (без ключа)..." -ForegroundColor Cyan

# Тест URL без ключа
$urlTest = @{ url = "https://www.google.com" } | ConvertTo-Json
Invoke-TestRequest -Method "POST" -Endpoint "/check/url" -Body $urlTest -TestName "URL Check (без ключа)"

# Тест файла без ключа
$fileTest = @{ file_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" } | ConvertTo-Json
Invoke-TestRequest -Method "POST" -Endpoint "/check/file" -Body $fileTest -TestName "File Check (без ключа)"

# Тест домена без ключа
Invoke-TestRequest -Method "GET" -Endpoint "/check/domain/google.com" -TestName "Domain Check (без ключа)"

Write-Host ""
Write-Host "3. 💎 Премиум функции (с ключом)..." -ForegroundColor Cyan

# Тест URL с ключом
Invoke-TestRequest -Method "POST" -Endpoint "/check/url" -Body $urlTest -ApiKey $PremiumApiKey -TestName "URL Check (с ключом)"

# Тест IP с ключом
Invoke-TestRequest -Method "GET" -Endpoint "/check/ip/8.8.8.8" -ApiKey $PremiumApiKey -TestName "IP Check (с ключом)"

# Тест анализа по наведению
$hoverTest = @{ url = "https://www.google.com"; domain = "google.com" } | ConvertTo-Json
Invoke-TestRequest -Method "POST" -Endpoint "/check/hover" -Body $hoverTest -ApiKey $PremiumApiKey -TestName "Hover Analysis (с ключом)"

Write-Host ""
Write-Host "4. 🎛️ Админ функции (без ключа)..." -ForegroundColor Cyan

# Тест статистики
Invoke-TestRequest -Method "GET" -Endpoint "/admin/stats" -TestName "Admin Stats (без ключа)"

# Тест добавления вредоносного хэша
Invoke-TestRequest -Method "POST" -Endpoint "/admin/add/malicious-hash" -Body "hash=test123&threat_type=malware&description=test" -TestName "Add Malicious Hash (без ключа)"

Write-Host ""
Write-Host "5. 🚫 Проверка блокировки премиум функций без ключа..." -ForegroundColor Cyan

# Попытка IP без ключа (должна быть ошибка)
try {
    $ipResult = Invoke-TestRequest -Method "GET" -Endpoint "/check/ip/8.8.8.8" -TestName "IP Check (без ключа - должна быть ошибка)"
    if ($ipResult) {
        Write-Host "  ⚠️ Неожиданно: IP проверен без ключа" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✅ Ожидаемо: IP проверка заблокирована без ключа" -ForegroundColor Green
}

# Попытка hover analysis без ключа (должна быть ошибка)
try {
    $hoverResult = Invoke-TestRequest -Method "POST" -Endpoint "/check/hover" -Body $hoverTest -TestName "Hover Analysis (без ключа - должна быть ошибка)"
    if ($hoverResult) {
        Write-Host "  ⚠️ Неожиданно: Hover analysis выполнен без ключа" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ✅ Ожидаемо: Hover analysis заблокирован без ключа" -ForegroundColor Green
}

Write-Host ""
Write-Host "🎉 Тестирование завершено!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Дополнительные ссылки:" -ForegroundColor Cyan
Write-Host "   Документация API: $BaseUrl/docs" -ForegroundColor Gray
Write-Host "   Админ панель: $BaseUrl/admin/ui" -ForegroundColor Gray
Write-Host "   Health check: $BaseUrl/health" -ForegroundColor Gray
