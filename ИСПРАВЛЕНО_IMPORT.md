# ✅ Исправлено: ImportError при запуске

## Проблема
```
ImportError: cannot import name 'logging_config' from 'app.config'
```

## Решение
Добавлен класс `LoggingConfig` и экземпляр `logging_config` в файл `antivirus-core/app/config.py`:

```python
class LoggingConfig:
    """Конфигурация логирования"""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_MAX_SIZE_MB = int(os.getenv("LOG_MAX_SIZE_MB", "10"))
    LOG_ROTATION_DAYS = int(os.getenv("LOG_ROTATION_DAYS", "7"))

logging_config = LoggingConfig()
```

## Что было добавлено
- ✅ Класс `LoggingConfig` с параметрами логирования
- ✅ Экземпляр `logging_config` для импорта в других модулях

## Параметры логирования
- `LOG_LEVEL` - уровень логирования (INFO по умолчанию)
- `LOG_MAX_SIZE_MB` - максимальный размер лог файла (10 МБ)
- `LOG_ROTATION_DAYS` - количество дней хранения логов (7 дней)

## Теперь сервер запускается!
Попробуйте снова:
```bash
python start_aegis.py
```
