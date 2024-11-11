# taskworker-analyzetext
TaskBridge worker for chatting with texts via large language models (LLM)

## Result format

When calling the TaskBridge `/api/tasks/complete/:id` API, the following JSON structure is sent to the endpoint.

```json
{
  "result" : {
    "messages": [
      {
        "role": "user",
        "content": "why is the sky blue?"
      },
      {
        "role": "assistant",
        "content": "due to rayleigh scattering."
      },
      {
        "role": "user",
        "content": "how is that different than mie scattering?"
      },
      {
        "role": "assistant",
        "content": "mie scattering occurs when light interacts with larger particles in the air."
      }
    ],
    "duration" : 1.6,
    "repository" : "https://github.com/hilderonny/taskworker-analyzetext",
    "version" : "1.0.0",
    "library": "Ollama 0.4",
    "model": "llama3.2"
  }
}
```

|Property|Description|
|---|---|
|`messages`|History of the chat messages with new answers|
|`messages.role`|Role of the message. `user` represents the quentionaire, the last message should be of this role. `assistant` contains responses from the LLM.|
|`messages.content`|Text content of the message|
|`duration`|Time in seconds for the processing|
|`repository`|Source code repository of the worker|
|`version`|Version of the worker|
|`library`|Library or application used for chatting|
|`model`|LLM model used|

## Installation on Windows

First download and install [Ollama](https://ollama.com/download). Open a shell and tell Ollama to download the model to use, e.g. `llama3.2`. This model is about 2 GB in size and requires about 4 GB of RAM or VRAM. See https://ollama.com/library for a list of available models.

```sh
ollama pull llama3.2
```

Next download and install [Python 3.13](https://www.python.org/downloads/release/python-3130/). Open a shell in this repository and prepare a virtual environment in this way.

```sh
python3.13 -m venv venv
venv\Scripts\activate
pip install ollama requests
```

## Running

```sh
venv\Scripts\activate
python analyzetext.py --taskbridgeurl http://192.168.178.39:42000/ --worker ROG --model llama3.2
```