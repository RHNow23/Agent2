# This script sends a request to the local Ollama API to generate a haiku about Python with streaming enabled.
# Option 2: Using requests (Raw API)
# This is slightly more manual because you have to process each JSON object as it arrives over the network.

######## Did NOT run, got permission denied error 12/15/25

import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.1:8b",
    "prompt": "Write a haiku about Python.",
    "stream": True  # Enable streaming here
}

# Make sure to set stream=True in the requests.post call as well
response = requests.post(url, json=data, stream=True)

for line in response.iter_lines():
    if line:
        # Decode the bytes to string and parse JSON
        decoded_line = json.loads(line.decode('utf-8'))
        
        # Print the 'response' part without a newline
        print(decoded_line['response'], end='', flush=True)

print()