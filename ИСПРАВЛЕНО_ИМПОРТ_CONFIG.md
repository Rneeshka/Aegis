# ✅ Исправлена ошибка импорта config

## Проблема:
```
ImportError: cannot import name 'logging_config' from 'app.config'
```

## Решение:

### 1. Добавлены недостающие классы в `config.py`:
```python
class LoggingConfig:
    """Конфигурация логирования"""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_MAX_SIZE_MB = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_ROTATION_DAYS = int(os.getenv("LOG_ROTATION_DAYS", "7"))

class SecurityConfig:
    """Конфигурация безопасности"""
    ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "admin_token_123")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    MAX_URL_LENGTH = int(os.getenv("MAX_URL_LENGTH", "2048"))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
```

### 2. Созданы экземпляры конфигураций:
```python
# Создаем экземпляры конфигураций
logging_config = LoggingConfig()
security_config = SecurityConfig()
external_config = ExternalAPIConfig()
```

### 3. Исправлен дублированный комментарий в `main.py`

## Способы запуска сервера:

### Вариант 1: Через Python скрипт
```bash
python run_server.py
```

### Вариант 2: Через bat файл (Windows)
```bash
run_server.bat
```

### Вариант 3: Напрямую через uvicorn
```bash
cd antivirus-core
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Вариант 4: Через start_aegis.py
```bash
python start_aegis.py
```

## Проверка работы:

После запуска сервера проверьте:
- **Статус**: http://127.0.0.1:8000/health
- **Документация**: http://127.0.0.1:8000/docs  
- **Admin UI**: http://127.0.0.1:8000/admin/ui

## Что исправлено:

1. ✅ **Импорт logging_config** - добавлен класс и экземпляр
2. ✅ **Импорт security_config** - добавлен класс и экземпляр  
3. ✅ **Дублированный комментарий** - убран из main.py
4. ✅ **Созданы скрипты запуска** - run_server.py и run_server.bat

Теперь сервер должен запускаться без ошибок! 🎉

## Проблема:
```
ImportError: cannot import name 'logging_config' from 'app.config'
```

## Решение:

### 1. Добавлены недостающие классы в `config.py`:
```python
class LoggingConfig:
    """Конфигурация логирования"""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_MAX_SIZE_MB = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_ROTATION_DAYS = int(os.getenv("LOG_ROTATION_DAYS", "7"))

class SecurityConfig:
    """Конфигурация безопасности"""
    ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "admin_token_123")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    MAX_URL_LENGTH = int(os.getenv("MAX_URL_LENGTH", "2048"))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
```

### 2. Созданы экземпляры конфигураций:
```python
# Создаем экземпляры конфигураций
logging_config = LoggingConfig()
security_config = SecurityConfig()
external_config = ExternalAPIConfig()
```

### 3. Исправлен дублированный комментарий в `main.py`

## Способы запуска сервера:

### Вариант 1: Через Python скрипт
```bash
python run_server.py
```

### Вариант 2: Через bat файл (Windows)
```bash
run_server.bat
```

### Вариант 3: Напрямую через uvicorn
```bash
cd antivirus-core
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Вариант 4: Через start_aegis.py
```bash
python start_aegis.py
```

## Проверка работы:

После запуска сервера проверьте:
- **Статус**: http://127.0.0.1:8000/health
- **Документация**: http://127.0.0.1:8000/docs  
- **Admin UI**: http://127.0.0.1:8000/admin/ui

## Что исправлено:

1. ✅ **Импорт logging_config** - добавлен класс и экземпляр
2. ✅ **Импорт security_config** - добавлен класс и экземпляр  
3. ✅ **Дублированный комментарий** - убран из main.py
4. ✅ **Созданы скрипты запуска** - run_server.py и run_server.bat

Теперь сервер должен запускаться без ошибок! 🎉

## Проблема:
```
ImportError: cannot import name 'logging_config' from 'app.config'
```

## Решение:

### 1. Добавлены недостающие классы в `config.py`:
```python
class LoggingConfig:
    """Конфигурация логирования"""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_MAX_SIZE_MB = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_ROTATION_DAYS = int(os.getenv("LOG_ROTATION_DAYS", "7"))

class SecurityConfig:
    """Конфигурация безопасности"""
    ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "admin_token_123")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    MAX_URL_LENGTH = int(os.getenv("MAX_URL_LENGTH", "2048"))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
```

### 2. Созданы экземпляры конфигураций:
```python
# Создаем экземпляры конфигураций
logging_config = LoggingConfig()
security_config = SecurityConfig()
external_config = ExternalAPIConfig()
```

### 3. Исправлен дублированный комментарий в `main.py`

## Способы запуска сервера:

### Вариант 1: Через Python скрипт
```bash
python run_server.py
```

### Вариант 2: Через bat файл (Windows)
```bash
run_server.bat
```

### Вариант 3: Напрямую через uvicorn
```bash
cd antivirus-core
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Вариант 4: Через start_aegis.py
```bash
python start_aegis.py
```

## Проверка работы:

После запуска сервера проверьте:
- **Статус**: http://127.0.0.1:8000/health
- **Документация**: http://127.0.0.1:8000/docs  
- **Admin UI**: http://127.0.0.1:8000/admin/ui

## Что исправлено:

1. ✅ **Импорт logging_config** - добавлен класс и экземпляр
2. ✅ **Импорт security_config** - добавлен класс и экземпляр  
3. ✅ **Дублированный комментарий** - убран из main.py
4. ✅ **Созданы скрипты запуска** - run_server.py и run_server.bat

Теперь сервер должен запускаться без ошибок! 🎉

## Проблема:
```
ImportError: cannot import name 'logging_config' from 'app.config'
```

## Решение:

### 1. Добавлены недостающие классы в `config.py`:
```python
class LoggingConfig:
    """Конфигурация логирования"""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_MAX_SIZE_MB = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_ROTATION_DAYS = int(os.getenv("LOG_ROTATION_DAYS", "7"))

class SecurityConfig:
    """Конфигурация безопасности"""
    ADMIN_API_TOKEN = os.getenv("ADMIN_API_TOKEN", "admin_token_123")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    MAX_URL_LENGTH = int(os.getenv("MAX_URL_LENGTH", "2048"))
    MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
```

### 2. Созданы экземпляры конфигураций:
```python
# Создаем экземпляры конфигураций
logging_config = LoggingConfig()
security_config = SecurityConfig()
external_config = ExternalAPIConfig()
```

### 3. Исправлен дублированный комментарий в `main.py`

## Способы запуска сервера:

### Вариант 1: Через Python скрипт
```bash
python run_server.py
```

### Вариант 2: Через bat файл (Windows)
```bash
run_server.bat
```

### Вариант 3: Напрямую через uvicorn
```bash
cd antivirus-core
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Вариант 4: Через start_aegis.py
```bash
python start_aegis.py
```

## Проверка работы:

После запуска сервера проверьте:
- **Статус**: http://127.0.0.1:8000/health
- **Документация**: http://127.0.0.1:8000/docs  
- **Admin UI**: http://127.0.0.1:8000/admin/ui

## Что исправлено:

1. ✅ **Импорт logging_config** - добавлен класс и экземпляр
2. ✅ **Импорт security_config** - добавлен класс и экземпляр  
3. ✅ **Дублированный комментарий** - убран из main.py
4. ✅ **Созданы скрипты запуска** - run_server.py и run_server.bat

Теперь сервер должен запускаться без ошибок! 🎉
