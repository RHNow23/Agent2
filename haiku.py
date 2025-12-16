# This script generates a haiku about Python using the Ollama API with streaming enabled.
# Make sure you have the Ollama library installed and properly configured.
# You can install it via pip if you haven't done so:
# pip install ollama
# successfully run 12/15/25


import ollama

# 1. Enable streaming
stream = ollama.chat(
    model='llama3.1:8b',
    messages=[{'role': 'user', 'content': 'Write a haiku about Python.'}],
    stream=True,
)

# 2. Loop through the chunks and print them instantly
for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

# Add a final newline for clean output
print()