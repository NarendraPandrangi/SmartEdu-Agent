import urllib.request
import json
import ssl

url = "https://cloud.olakrutrim.com/v1/chat/completions"
headers = {
    "Authorization": "Bearer 6CIYq3OVlXswA9FW4eME6Hqv",
    "Content-Type": "application/json"
}
data = {
    "model": "Krutrim-spectre-v2",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers)
context = ssl._create_unverified_context()

try:
    with urllib.request.urlopen(req, context=context) as res:
        print(f"Status: {res.status}")
        print(res.read().decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
