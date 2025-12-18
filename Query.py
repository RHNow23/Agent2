
import ollama

# Define the model you have installed (e.g., 'llama3.2', 'mistral', 'llama3')
# llama3.1:8b

desired_model = 'llama3.1:8b'  # Change this to the model you have installed

response = ollama.chat(model=desired_model, messages=[
  {
    'role': 'user',
    'content': 'how do I retrieve stored text in the model?',
  },
])

# Retrieve and print the specific text content
generated_text = response['message']['content']
print(f"--- Response from {desired_model} ---\n")
print(generated_text)