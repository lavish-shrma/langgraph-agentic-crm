import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://localhost:8000/api/interactions')
    print("SUCCESS:")
    print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTP ERROR {e.code}:")
    print(e.read().decode())
except Exception as e:
    print(f"ERROR: {e}")
