
Conversation with Gemini
simple way to ask question of model in ollama using python and wsl
Here is the simplest way to ask a question of an Ollama model using Python in WSL (Windows Subsystem for Linux).
Prerequisite
Before running the Python script, ensure Ollama is running in your WSL terminal.
1.	Open a terminal in WSL.
2.	Run the server (if it isn't already running in the background):
Bash
ollama serve
3.	Ensure you have pulled the model you want to use (e.g., ollama pull llama3).
________________________________________
Option 1: Using the Official Ollama Library (Recommended)
This is the cleanest and easiest method.
1. Install the library: Run this in your WSL terminal:
Bash
pip install ollama
2. Create the Python script (e.g., chat.py):
Python
import ollama

response = ollama.chat(model='llama3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response['message']['content'])
3. Run it:
Bash
python chat.py
________________________________________
Option 2: Using the requests Library
Use this if you don't want to install the specific Ollama library and prefer standard HTTP requests.
1. Install requests (if not installed):
Bash
pip install requests
2. Create the Python script (e.g., chat_api.py):
Python
import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3",
    "prompt": "Why is the sky blue?",
    "stream": False  # Set to True if you want to stream the response
}

response = requests.post(url, json=data)

# Print the actual text response
print(response.json()['response'])
________________________________________
Troubleshooting
•	Connection Error: If you get a connection refused error, make sure ollama serve is running in a separate terminal window or in the background.
•	Model Not Found: Ensure the "model" name in the script matches exactly what you see when you run ollama list in the terminal.
Would you like to see how to stream the response (print words as they are generated) so it feels faster?

Here is how to stream the response so it appears token-by-token, similar to how ChatGPT or the terminal interface works.

Option 1: Using the Official Library (Simplest)
You simply add stream=True and loop through the results.

Python

import ollama

# 1. Enable streaming
stream = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': 'Write a haiku about Python.'}],
    stream=True,
)

# 2. Loop through the chunks and print them instantly
for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

# Add a final newline for clean output
print()
Option 2: Using requests (Raw API)
This is slightly more manual because you have to process each JSON object as it arrives over the network.

Python

import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3",
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
Why use flush=True?
Python usually "buffers" output (saves it up to print in blocks) to be more efficient. flush=True forces Python to write the text to the screen immediately, which creates that smooth typing effect.

Would you like to know how to save this conversation history so the model "remembers" what you said in the next turn?

yes

To make the model "remember" previous turns, you must manage the history yourself. Ollama models are stateless—they don't remember what you said 5 seconds ago unless you send the entire conversation log back to them with every new question.

Here is a script that creates a continuous chat loop with memory.

Python Script with Memory
This script keeps a list called messages and appends every User question and AI answer to it.

Python
import ollama

# 1. Initialize an empty list to store conversation history
messages = []

print("Chat with Ollama (type 'exit' to quit)")
print("-" * 40)

while True:
    # 2. Get user input
    user_input = input("You: ")
    
    # Allow the user to quit
    if user_input.lower() == 'exit':
        break

    # 3. Add the user's message to history
    messages.append({'role': 'user', 'content': user_input})

    # 4. Send the FULL history to the model
    stream = ollama.chat(
        model='llama3', 
        messages=messages, 
        stream=True
    )

    print("AI: ", end='', flush=True)

    # We need to build the full response string to save it later
    full_response = ""
    
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_response += content

    print("\n") # New line after response

    # 5. Add the AI's response to history so it remembers it next time
    messages.append({'role': 'assistant', 'content': full_response})
Key Concepts
The List (messages): This is the brain. It looks like this after a few turns:

Python
[
  {'role': 'user', 'content': 'Hi, my name is Dave.'},
  {'role': 'assistant', 'content': 'Hello Dave!'},
  {'role': 'user', 'content': 'What is my name?'} 
]
The Role: You must label who said what using 'role': 'user' or 'role': 'assistant'.

Limitation
The "context window" (the amount of text the model can handle) is finite. If you talk for hours, this list will eventually get too big for the model to process, and it will crash or forget the beginning.

Would you like to know how to add a System Prompt to give the AI a specific personality (e.g., "You are a helpful coding assistant" or "You are a pirate")?