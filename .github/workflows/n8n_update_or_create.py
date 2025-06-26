import requests
import json
import os

N8N_HOST = os.environ["N8N_HOST"]
N8N_API_KEY = os.environ["N8N_API_KEY"]
WORKFLOW_FILE = "telegram_echo_workflow.json"

with open(WORKFLOW_FILE, "r", encoding="utf-8") as f:
    workflow_data = json.load(f)

response = requests.get(f"{N8N_HOST}/api/v1/workflows", headers={"X-N8N-API-KEY": N8N_API_KEY})
workflows = response.json()["data"] if "data" in response.json() else response.json()
target = next((w for w in workflows if w.get("name") == workflow_data["name"]), None)
if target:
    workflow_id = target["id"]
    r = requests.patch(
        f"{N8N_HOST}/rest/workflows/{workflow_id}",
        headers={"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"},
        data=json.dumps(workflow_data)
    )
    print("PATCH status:", r.status_code)
    print("Ответ:", r.text)
else:
    r = requests.post(
        f"{N8N_HOST}/api/v1/workflows",
        headers={"X-N8N-API-KEY": N8N_API_KEY, "Content-Type": "application/json"},
        data=json.dumps(workflow_data)
    )
    print("POST status:", r.status_code)
    print("Ответ:", r.text) 