import requests
import json
import os

N8N_HOST = os.environ["N8N_HOST"]
N8N_API_KEY = os.environ["N8N_API_KEY"]
WORKFLOW_FILE = "telegram_echo_workflow.json"

with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
    new_data = json.load(f)

# Получаем список всех воркфлоу
response = requests.get(
    f"{N8N_HOST}/api/v1/workflows",
    headers={"X-N8N-API-KEY": N8N_API_KEY}
)
workflows = response.json()["data"] if "data" in response.json() else response.json()
target = next((w for w in workflows if w.get("name") == new_data["name"]), None)

# Разрешённые поля по OpenAPI: name, nodes, connections, settings, staticData
# Для активации используйте POST /workflows/{id}/activate
# Для тегов используйте PUT /workflows/{id}/tags

def filter_fields(obj):
    allowed = ["name", "nodes", "connections", "settings", "staticData"]
    return {k: v for k, v in obj.items() if k in allowed}

if target:
    workflow_id = target["id"]
    # Получаем полный объект воркфлоу
    current = requests.get(
        f"{N8N_HOST}/api/v1/workflows/{workflow_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    ).json()
    # Обновляем только нужные поля
    current["nodes"] = new_data["nodes"]
    current["connections"] = new_data["connections"]
    current["settings"] = new_data.get("settings", {})
    current["name"] = new_data["name"]
    # Оставляем только разрешённые поля (строго по OpenAPI)
    payload = filter_fields(current)
    print(f"Workflow '{new_data['name']}' найден, обновляю...")
    r = requests.put(
        f"{N8N_HOST}/api/v1/workflows/{workflow_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    print(f"PUT /api/v1/workflows/{workflow_id} -> {r.status_code}")
    print("Ответ сервера:")
    print(r.text)
else:
    print(f"Workflow '{new_data['name']}' не найден, создаю новый...")
    r = requests.post(
        f"{N8N_HOST}/api/v1/workflows",
        headers={"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"},
        data=json.dumps(filter_fields(new_data))
    )
    print(f"POST /api/v1/workflows -> {r.status_code}")
    print("Ответ сервера:")
    print(r.text) 