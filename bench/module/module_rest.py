import requests
import time
import json

def predict(server_address, model_name, data):
    headers = {"content-type": "application/json"}
    url = server_address + "v1/models/" + model_name + ":predict"
    request_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time()
    elapsed_time = response_time - request_time
    result = json.loads(response.text)
    return result, elapsed_time
