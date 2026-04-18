from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
try:
    response = client.get("/api/interactions")
    print("STATUS:", response.status_code)
    print("JSON:", response.json())
except Exception as e:
    import traceback
    traceback.print_exc()
