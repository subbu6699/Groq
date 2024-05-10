import requests
import os

api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error fetching models: {response.status_code} - {response.text}")
