#!/bin/bash
cd /opt/Aegis || exit

# Добавляем все изменения
git add .

# Создаём коммит с текущей датой
git commit -m "Auto backup on $(date '+%Y-%m-%d %H:%M:%S')" >/dev/null 2>&1

# Отправляем на GitHub
git push origin main
