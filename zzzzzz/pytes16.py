import requests
import os

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')  # Make sure to set your environment variable

def generate_tests(url):
    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "gemini-model",  # Use the correct model name if available
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate pytest code for the FastAPI application with endpoints at {url}"}
        ],
        "max_tokens": 150
    }
    api_url = 'https://api.gemini.com/v1/completions'  # Replace with the correct endpoint
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Check for request errors
    return response.json()['choices'][0]['message']['content']

# Example usage
url = "http://localhost:8000"
pytest_code = generate_tests(url)
print(pytest_code)
