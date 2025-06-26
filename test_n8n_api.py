import os
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env, если он есть
load_dotenv()

N8N_HOST = os.getenv("N8N_HOST")
N8N_API_KEY = os.getenv("N8N_API_KEY")
WORKFLOW_FILE = "telegram_echo_workflow.json"

if not N8N_HOST or not N8N_API_KEY:
    print("Пожалуйста, укажите N8N_HOST и N8N_API_KEY в .env или переменных окружения.")
    exit(1)

# Проверка доступности API
print("Проверка доступности API...")
r = requests.get(f"{N8N_HOST}/api/v1/workflows", headers={
    "X-N8N-API-KEY": N8N_API_KEY
})
print(f"GET /api/v1/workflows -> {r.status_code}")

# Тестовый POST (создание воркфлоу)
print("Пробую отправить workflow...")
with open(WORKFLOW_FILE, "rb") as f:
    data = f.read()
r = requests.post(f"{N8N_HOST}/api/v1/workflows",
                  headers={
                      "X-N8N-API-KEY": N8N_API_KEY,
                      "Content-Type": "application/json"
                  },
                  data=data)
print(f"POST /api/v1/workflows -> {r.status_code}")
print("Ответ сервера:")
print(r.text) 