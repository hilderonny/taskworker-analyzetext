from importlib.metadata import version
import time
import json
import requests
import datetime
import argparse

REPOSITORY = "https://github.com/hilderonny/taskworker-analyzetext"
VERSION = "1.0.0"
LIBRARY = "ollama-" + version("ollama")

print(f'taskworker-analyzetext {VERSION}')

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--taskbridgeurl', type=str, action='store', required=True, help='Root URL of the API of the task bridge to use, e.g. https://taskbridge.ai/')
parser.add_argument('--model', type=str, action='store', help='LLM Model to use. See https://ollama.com/library for available models.')
parser.add_argument('--version', '-v', action='version', version=VERSION)
parser.add_argument('--worker', type=str, action='store', required=True, help='Unique name of this worker')
args = parser.parse_args()

WORKER = args.worker
print(f'Worker name: {WORKER}')
TASKBRIDGEURL = args.taskbridgeurl
if not TASKBRIDGEURL.endswith("/"):
    TASKBRIDGEURL = f"{TASKBRIDGEURL}/"
APIURL = f"{TASKBRIDGEURL}api/"
print(f'Using API URL {APIURL}')

MODEL = args.model
print(f'Using LLM model {MODEL}')

# Load AI
import ollama

def check_and_process():
    start_time = datetime.datetime.now()
    take_request = {}
    take_request["type"] = "analyzetext"
    take_request["worker"] = WORKER
    response = requests.post(f"{APIURL}tasks/take/", json=take_request)
    if response.status_code != 200:
        return False
    task = response.json()
    taskid = task["id"]
    messages = task["data"]["messages"]

    llmresponse = ollama.chat(model=MODEL, messages=messages)
    messages.append(llmresponse["message"])

    result_to_report = {}
    result_to_report["result"] = {}
    result_to_report["result"]["messages"] = messages
    end_time = datetime.datetime.now()
    result_to_report["result"]["duration"] = (end_time - start_time).total_seconds()
    result_to_report["result"]["repository"] = REPOSITORY
    result_to_report["result"]["version"] = VERSION
    result_to_report["result"]["library"] = LIBRARY
    result_to_report["result"]["model"] = MODEL
    print(json.dumps(result_to_report, indent=2))
    print("Reporting result")
    requests.post(f"{APIURL}tasks/complete/{taskid}/", json=result_to_report)
    print("Done")
    return True

try:
    print('Ready and waiting for action')
    while True:
        task_was_processed = False
        try:
            task_was_processed = check_and_process()
        except Exception as ex:
            print(ex)
        if task_was_processed == False:
            time.sleep(3)
except Exception:
    pass
