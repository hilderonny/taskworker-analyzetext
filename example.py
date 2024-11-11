import ollama
import json

response = ollama.chat(model="llama3.2", messages=[
  {
    "role": "user",
    "content": "Warum ist der Himmel blau?",
  },
])

print(json.dumps(response, indent=2))
