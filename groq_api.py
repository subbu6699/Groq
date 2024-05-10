# groq_api.py
import requests

class GroqAPI:
    def __init__(self, api_key, base_url="https://api.groq.com"):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.base_url = base_url

    def get_available_models(self):
        """Fetch a list of available models from the Groq API."""
        url = f"{self.base_url}/models"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json().get('models', [])
        else:
            return f"Error: {response.status_code} - {response.text}"

    def chat_with_model(self, model_id, input_text):
        """Send a message to the specified model and return its response."""
        url = f"{self.base_url}/models/{model_id}/chat"
        payload = {
            "input": input_text
        }
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 200:
            return response.json().get('output', 'No response')
        else:
            return f"Error: {response.status_code} - {response.text}"
