import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_chat(message):
    print(f"\n[{time.strftime('%H:%M:%S')}] --- Test Message: {message} ---")
    try:
        response = requests.post(
            f"{BASE_URL}/agent/chat",
            json={"message": message, "conversation_history": []},
            timeout=300
        )
        print(f"[{time.strftime('%H:%M:%S')}] Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
        # Wait for rate limit window to reset slightly
        print("Waiting 30s for rate limit window...")
        time.sleep(30)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Test 1
    test_chat("Schedule a follow-up with Dr. Ananya Iyer on 2026-05-20 to discuss latest neurology clinical data.")
    
    # Test 2
    test_chat("Summarize my last 3 visits with Dr. Vikram Patel.")
    
    # Test 3
    test_chat("Show me the full profile for Dr. Priya Sharma.")
