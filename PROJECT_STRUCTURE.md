# 🏗️ Структура проекта Aegis

## 📁 Основные папки

### `aegis_start/` - Фронтенд (Браузерное расширение)
```
aegis_start/
├── manifest.json          # Манифест расширения
├── background.js           # Service Worker
├── content_script.js       # Скрипт для веб-страниц
├── popup.html              # Интерфейс popup
├── popup.js                # Логика popup
├── options.html            # Страница настроек
├── options.js              # Логика настроек
├── icons/                  # Иконки расширения
│   ├── icon-48.png
│   └── icon-128.png
├── native_host/           # Native Host для расширения
│   ├── host-manifest-chrome.json
│   └── native_host.py
└── docs/                   # Документация расширения
    ├── native-host-registration.md
    └── privacy-policy-template.md
```

### `antivirus-core/` - Бэкенд (API сервер)
```
antivirus-core/
├── app/                    # Основной код приложения
│   ├── __init__.py
│   ├── main.py             # FastAPI приложение
│   ├── config.py           # Конфигурация
│   ├── database.py          # Работа с БД
│   ├── services.py          # Бизнес-логика
│   ├── logger.py            # Логирование
│   ├── schemas.py           # Pydantic модели
│   ├── validators.py        # Валидация
│   ├── security.py          # Безопасность
│   ├── cache.py             # Кэширование
│   ├── background_jobs.py   # Фоновые задачи
│   ├── admin_ui.py          # Админ панель
│   ├── env.env              # Переменные окружения
│   ├── external_apis/       # Внешние API
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   ├── base_client.py
│   │   ├── virustotal.py
│   │   ├── google_safe_browsing.py
│   │   └── abuseipdb.py
│   └── static/              # Статические файлы
│       └── admin/
│           └── index.html
├── data/                   # Базы данных
│   ├── antivirus.db
│   ├── antivirus.db-shm
│   ├── antivirus.db-wal
│   └── cache.db
├── logs/                   # Логи приложения
├── requirements.txt        # Python зависимости
├── run_local.ps1          # Скрипт запуска
└── *.md                   # Документация
```

## 📁 Вспомогательные папки

### `docs/` - Общая документация
```
docs/
├── README.md              # Основная документация
├── STRUCTURE.md           # Структура проекта
└── QUICK_START.md         # Быстрый старт
```

### `scripts/` - Утилиты и скрипты
```
scripts/
├── start_server.py        # Запуск сервера
├── install_extension.py   # Установка расширения
└── check_structure.py     # Проверка структуры
```

### `tests/` - Тесты
```
tests/
└── test_api.py           # Тесты API
```

## 🗑️ Файлы для удаления

Следующие файлы являются дубликатами или временными:
- `backend/` (дубликат)
- `frontend/` (дубликат) 
- `data/` в корне (дубликат)
- `logs/` в корне (дубликат)
- `admin_ui_simple.html` (временный)
- `*.md` в корне (кроме README.md)
- `quick_test.py`
- `run_server.py`
- `start_server_and_test.py`
- `test_admin_api.py`
- `*.md` файлы с исправлениями

