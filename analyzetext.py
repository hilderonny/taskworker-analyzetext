import ollama
response = ollama.chat(model="llama3.2", messages=[
  {
    "role": "user",
    "content": "Warum ist der Himmel blau?",
  },
])
print(response["message"]["content"])