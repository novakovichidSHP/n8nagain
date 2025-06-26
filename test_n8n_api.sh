#!/bin/bash

# Загрузка переменных из .env, если файл существует
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Если переменные не заданы, просим пользователя
if [ -z "$N8N_HOST" ] || [ -z "$N8N_API_KEY" ]; then
  echo "Пожалуйста, укажите N8N_HOST и N8N_API_KEY в .env или в переменных окружения."
  exit 1
fi

WORKFLOW_FILE="telegram_echo_workflow.json"

# Проверка доступности API
echo "Проверка доступности API..."
curl -s -o /dev/null -w "%{http_code}\n" "$N8N_HOST/api/v1/workflows"

# Тестовый POST (создание воркфлоу)
echo "Пробую отправить workflow..."
curl -v -X POST "$N8N_HOST/api/v1/workflows" \
  -H "Authorization: Bearer $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @"$WORKFLOW_FILE" 