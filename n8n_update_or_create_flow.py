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
    print(f"Workflow '{new_data['name']}' найден, обновляю...")
    # Получаем полный объект воркфлоу
    current = requests.get(
        f"{N8N_HOST}/api/v1/workflows/{workflow_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    ).json()
    current["nodes"] = new_data["nodes"]
    current["connections"] = new_data["connections"]
    current["settings"] = new_data.get("settings", {})
    current["name"] = new_data["name"]
    # Оставляем только разрешённые поля (строго по OpenAPI)
    payload = filter_fields(current)
    r = requests.put(
        f"{N8N_HOST}/api/v1/workflows/{workflow_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"},
        data=json.dumps(payload)
    )
    print(f"PUT /api/v1/workflows/{workflow_id} -> {r.status_code}")
    print("Ответ сервера:")
    print(r.text)
    # Автоматическая активация воркфлоу
    activate = requests.post(
        f"{N8N_HOST}/api/v1/workflows/{workflow_id}/activate",
        headers={"X-N8N-API-KEY": N8N_API_KEY}
    )
    print(f"POST /api/v1/workflows/{workflow_id}/activate -> {activate.status_code}")
    print(activate.text)
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
    # Автоматическая активация нового воркфлоу
    if r.status_code == 200:
        workflow_id = r.json().get("id")
        if workflow_id:
            activate = requests.post(
                f"{N8N_HOST}/api/v1/workflows/{workflow_id}/activate",
                headers={"X-N8N-API-KEY": N8N_API_KEY}
            )
            print(f"POST /api/v1/workflows/{workflow_id}/activate -> {activate.status_code}")
            print(activate.text) 