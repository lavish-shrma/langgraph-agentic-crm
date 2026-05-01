import requests
import json
import time

url = "http://127.0.0.1:8000/api/agent/chat"
headers = {"Content-Type": "application/json"}
data = {
    "message": "Summarize my last 3 visits with Dr. Vikram Patel.",
    "conversation_history": []
}

for i in range(5):
    try:
        response = requests.post(url, headers=headers, json=data)
        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
        break
    except Exception as e:
        print("Waiting for server to start...", e)
        time.sleep(2)
