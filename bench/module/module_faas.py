import requests
import time

def predict(server_address, data):
    headers = {"content-type": "application/json"}
    url = server_address
    request_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time()
    elapsed_time = response_time - request_time
    result = response.json()
    return result, elapsed_time
