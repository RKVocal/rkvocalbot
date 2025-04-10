#!/bin/bash

# Задай свой GitHub токен и репозиторий
GITHUB_USER="rkvocal"
GITHUB_TOKEN=""
REPO_NAME="rkvocalbot"

# Удаляем origin, если он уже есть
git remote remove origin 2> /dev/null

# Добавляем origin с токеном
git remote add origin https://$GITHUB_USER:$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git

# Добавляем файлы, коммитим, пушим
git add .
git commit -m "🔄 Автоматический пуш с Replit" || echo "⏩ Нет новых изменений"
git push -u origin main
