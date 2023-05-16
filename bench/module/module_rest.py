import requests
import time

def predict(server_address, model_name, data, using_lambda=0):
    headers = {"content-type": "application/json"}
    url = server_address + "v1/models/" + model_name + ":predict"
    request_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time()
    elapsed_time = response_time - request_time
    result = ""
    if (using_lambda == 1):
        result = response.json()
    else:
        result = response.text
    return result, elapsed_time
