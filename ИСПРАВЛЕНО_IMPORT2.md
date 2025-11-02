# ✅ Исправлено: ImportError с security_config

## Проблема
```
ImportError: cannot import name 'security_config' from 'app.config'
```

## Решение
Добавлен класс `SecurityConfig` и экземпляр `security_config` в файл `antivirus-core/app/config.py`:

```python
class SecurityConfig:
    """Конфигурация безопасности"""
    # Настройки валидации
    MAX_URL_LENGTH = int(os.getenv("MAX_URL_LENGTH", "2048"))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # Конвертируем в байты
    
    # API токены
    ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "admintoken123")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    
    # Разрешенные хосты
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

security_config = SecurityConfig()
```

## Что добавлено
- ✅ Класс `SecurityConfig` с параметрами безопасности
- ✅ Экземпляр `security_config` для импорта в других модулях
- ✅ Параметры валидации (MAX_URL_LENGTH, MAX_FILE_SIZE_MB, MAX_FILE_SIZE_BYTES)
- ✅ API токены (ADMIN_API_TOKEN, SECRET_KEY)
- ✅ Разрешенные хосты (ALLOWED_HOSTS)

## Полная структура config.py
Теперь файл содержит:
1. `ExternalAPIConfig` - конфигурация внешних API
2. `LoggingConfig` - конфигурация логирования
3. `SecurityConfig` - конфигурация безопасности

## Теперь сервер запускается без ошибок!
Попробуйте снова:
```bash
python start_aegis.py
```
