import requests
import json
import os

N8N_HOST = os.environ["N8N_HOST"]
N8N_API_KEY = os.environ["N8N_API_KEY"]
WORKFLOW_FILE = "telegram_echo_workflow.json"

with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
    workflow_data = json.load(f)

print("Пробую создать новый workflow...")
r = requests.post(
    f"{N8N_HOST}/api/v1/workflows",
    headers={"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"},
    data=json.dumps(workflow_data)
)
print(f"POST /api/v1/workflows -> {r.status_code}")
print("Ответ сервера:")
print(r.text) 