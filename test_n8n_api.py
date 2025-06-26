import os
import requests
import json
from dotenv import load_dotenv

# Загружаем переменные из .env, если он есть
load_dotenv()

N8N_HOST = os.getenv("N8N_HOST")
N8N_API_KEY = os.getenv("N8N_API_KEY")
WORKFLOW_FILE = "telegram_echo_workflow.json"

if not N8N_HOST or not N8N_API_KEY:
    print("Пожалуйста, укажите N8N_HOST и N8N_API_KEY в .env или переменных окружения.")
    exit(1)

with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
    workflow_data = json.load(f)

# 1. Получаем список всех воркфлоу
print("Проверка доступности API...")
response = requests.get(f"{N8N_HOST}/api/v1/workflows", headers={"X-N8N-API-KEY": N8N_API_KEY})
print(f"GET /api/v1/workflows -> {response.status_code}")
if response.status_code != 200:
    print("Ошибка при получении списка воркфлоу:", response.text)
    exit(1)
workflows = response.json()["data"] if "data" in response.json() else response.json()

# 2. Ищем воркфлоу с нужным именем
target = next((w for w in workflows if w.get("name") == workflow_data["name"]), None)

if target:
    # 3. Если найден — обновляем (PATCH)
    workflow_id = target["id"]
    print(f"Workflow '{workflow_data['name']}' найден, обновляю...")
    r = requests.patch(
        f"{N8N_HOST}/rest/workflows/{workflow_id}",
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        data=json.dumps(workflow_data)
    )
    print(f"PATCH /rest/workflows/{workflow_id} -> {r.status_code}")
    print("Ответ сервера:")
    print(r.text)
else:
    # 4. Если не найден — создаём новый (POST)
    print(f"Workflow '{workflow_data['name']}' не найден, создаю новый...")
    r = requests.post(
        f"{N8N_HOST}/api/v1/workflows",
        headers={
            "X-N8N-API-KEY": N8N_API_KEY,
            "Content-Type": "application/json"
        },
        data=json.dumps(workflow_data)
    )
    print(f"POST /api/v1/workflows -> {r.status_code}")
    print("Ответ сервера:")
    print(r.text) 