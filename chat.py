# questions ollama
# This code demonstrates how to use the Ollama library to interact with a language model.
## Make sure you have the Ollama library installed and properly configured.
# You can install it via pip if you haven't done so:
# pip install ollama
# successfully run 12/15/25

import ollama

response = ollama.chat(model='llama3.1:8b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response['message']['content'])
