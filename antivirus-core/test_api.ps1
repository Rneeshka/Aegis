# test_api.ps1
# Скрипт для тестирования API антивируса

param(
    [string]$BaseUrl = "http://127.0.0.1:9000",
    [string]$PremiumApiKey = "PREMI-12345-67890-ABCDE-FGHIJ-KLMNO"
)

Write-Host "🧪 Тестирование Antivirus Core API" -ForegroundColor Cyan
Write-Host "Base URL: $BaseUrl" -ForegroundColor Gray
Write-Host "Premium API Key: $PremiumApiKey" -ForegroundColor Gray
Write-Host ""

# Функция для выполнения HTTP запросов
function Invoke-ApiRequest {
    param(
        [string]$Method,
        [string]$Endpoint,
        [hashtable]$Headers = @{},
        [string]$Body = $null,
        [string]$ApiKey = $null
    )
    
    $url = "$BaseUrl$Endpoint"
    if ($ApiKey) {
        $headers["X-API-Key"] = $ApiKey
    }
    
    try {
        if ($Body) {
            $response = Invoke-RestMethod -Uri $url -Method $Method -Headers $Headers -Body $Body -ContentType "application/json"
        } else {
            $response = Invoke-RestMethod -Uri $url -Method $Method -Headers $Headers
        }
        return $response
    } catch {
        Write-Host "❌ Ошибка: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

# Тест 1: Health Check
Write-Host "1. 🔍 Проверка состояния системы..." -ForegroundColor Yellow
$health = Invoke-ApiRequest -Method "GET" -Endpoint "/health"
if ($health) {
    Write-Host "✅ Система работает" -ForegroundColor Green
    Write-Host "   База данных: $($health.database)" -ForegroundColor Gray
    Write-Host "   Внешние API: $($health.external_apis | ConvertTo-Json -Compress)" -ForegroundColor Gray
} else {
    Write-Host "❌ Система недоступна" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Тест 2: Проверка URL без ключа (базовый доступ)
Write-Host "2. 🌐 Проверка URL без ключа (базовый доступ)..." -ForegroundColor Yellow
$urlTest = @{
    url = "https://www.google.com"
} | ConvertTo-Json

$urlResult = Invoke-ApiRequest -Method "POST" -Endpoint "/check/url" -Body $urlTest
if ($urlResult) {
    Write-Host "✅ URL проверен (базовый доступ)" -ForegroundColor Green
    Write-Host "   Безопасен: $($urlResult.safe)" -ForegroundColor Gray
    Write-Host "   Источник: $($urlResult.source)" -ForegroundColor Gray
} else {
    Write-Host "❌ Ошибка проверки URL" -ForegroundColor Red
}

# Тест 2.1: Проверка URL с премиум ключом (расширенный доступ)
Write-Host "2.1. 🌐 Проверка URL с премиум ключом (расширенный доступ)..." -ForegroundColor Yellow
$urlResultPremium = Invoke-ApiRequest -Method "POST" -Endpoint "/check/url" -Body $urlTest -ApiKey $PremiumApiKey
if ($urlResultPremium) {
    Write-Host "✅ URL проверен (премиум доступ)" -ForegroundColor Green
    Write-Host "   Безопасен: $($urlResultPremium.safe)" -ForegroundColor Gray
    Write-Host "   Источник: $($urlResultPremium.source)" -ForegroundColor Gray
} else {
    Write-Host "❌ Ошибка проверки URL с премиум ключом" -ForegroundColor Red
}

Write-Host ""

# Тест 3: Проверка файла по хэшу
Write-Host "3. 📁 Проверка файла по хэшу..." -ForegroundColor Yellow
$hashTest = @{
    file_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
} | ConvertTo-Json

$hashResult = Invoke-ApiRequest -Method "POST" -Endpoint "/check/file" -Body $hashTest
if ($hashResult) {
    Write-Host "✅ Хэш проверен" -ForegroundColor Green
    Write-Host "   Безопасен: $($hashResult.safe)" -ForegroundColor Gray
    Write-Host "   Источник: $($hashResult.source)" -ForegroundColor Gray
} else {
    Write-Host "❌ Ошибка проверки хэша" -ForegroundColor Red
}

Write-Host ""

# Тест 4: Проверка IP адреса
Write-Host "4. 🌍 Проверка IP адреса..." -ForegroundColor Yellow
$ipResult = Invoke-ApiRequest -Method "GET" -Endpoint "/check/ip/8.8.8.8"
if ($ipResult) {
    Write-Host "✅ IP проверен" -ForegroundColor Green
    Write-Host "   Безопасен: $($ipResult.safe)" -ForegroundColor Gray
    Write-Host "   Источник: $($ipResult.source)" -ForegroundColor Gray
} else {
    Write-Host "❌ Ошибка проверки IP" -ForegroundColor Red
}

Write-Host ""

# Тест 5: Проверка IP адреса (требует премиум ключ)
Write-Host "5. 🌍 Проверка IP адреса (премиум функция)..." -ForegroundColor Yellow
$ipResult = Invoke-ApiRequest -Method "GET" -Endpoint "/check/ip/8.8.8.8" -ApiKey $PremiumApiKey
if ($ipResult) {
    Write-Host "✅ IP проверен (премиум)" -ForegroundColor Green
    Write-Host "   Безопасен: $($ipResult.safe)" -ForegroundColor Gray
    Write-Host "   Источник: $($ipResult.source)" -ForegroundColor Gray
} else {
    Write-Host "❌ Ошибка проверки IP" -ForegroundColor Red
}

# Тест 5.1: Попытка проверки IP без ключа (должна быть ошибка)
Write-Host "5.1. 🚫 Попытка проверки IP без ключа (должна быть ошибка)..." -ForegroundColor Yellow
try {
    $ipResultNoKey = Invoke-ApiRequest -Method "GET" -Endpoint "/check/ip/8.8.8.8"
    Write-Host "⚠️ Неожиданно: IP проверен без ключа" -ForegroundColor Yellow
} catch {
    Write-Host "✅ Ожидаемо: IP проверка заблокирована без ключа" -ForegroundColor Green
}

Write-Host ""

# Тест 6: Анализ по наведению (требует премиум ключ)
Write-Host "6. 🎯 Анализ по наведению (премиум функция)..." -ForegroundColor Yellow
$hoverTest = @{
    url = "https://www.google.com"
    domain = "google.com"
} | ConvertTo-Json

$hoverResult = Invoke-ApiRequest -Method "POST" -Endpoint "/check/hover" -Body $hoverTest -ApiKey $PremiumApiKey
if ($hoverResult) {
    Write-Host "✅ Анализ по наведению выполнен" -ForegroundColor Green
    Write-Host "   Результаты: $($hoverResult.results | ConvertTo-Json -Compress)" -ForegroundColor Gray
} else {
    Write-Host "❌ Ошибка анализа по наведению" -ForegroundColor Red
}

Write-Host ""

# Тест 6: Статистика базы данных
Write-Host "6. 📊 Статистика базы данных..." -ForegroundColor Yellow
$stats = Invoke-ApiRequest -Method "GET" -Endpoint "/admin/stats"
if ($stats) {
    Write-Host "✅ Статистика получена" -ForegroundColor Green
    Write-Host "   Вредоносные хэши: $($stats.stats.malicious_hashes)" -ForegroundColor Gray
    Write-Host "   Вредоносные URL: $($stats.stats.malicious_urls)" -ForegroundColor Gray
    Write-Host "   Активные ключи: $($stats.stats.active_api_keys)" -ForegroundColor Gray
} else {
    Write-Host "❌ Ошибка получения статистики" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 Тестирование завершено!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Дополнительные команды:" -ForegroundColor Cyan
Write-Host "   Документация API: $BaseUrl/docs" -ForegroundColor Gray
Write-Host "   Админ панель: $BaseUrl/admin/ui" -ForegroundColor Gray
Write-Host "   Health check: $BaseUrl/health" -ForegroundColor Gray
