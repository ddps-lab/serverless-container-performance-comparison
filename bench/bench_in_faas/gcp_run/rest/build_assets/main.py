import os
import time
import boto3
import requests
import json
from fastapi import FastAPI
app = FastAPI()

aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['AWS_REGION']

def predict(server_address, data):
    headers = {"content-type": "application/json"}
    url = server_address
    request_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time()
    network_latency_time = response_time - request_time
    result = response.json()
    return result, network_latency_time

def create_log_event(log_group_name, log_stream_name, inference_time, network_latency_time):
    logs_client = boto3.client('logs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    log_data = {
        'inference_time': inference_time,
        'network_latency_time': network_latency_time
    }
    log_event = {
        'timestamp':int (time.time() * 1000),
        'message': json.dumps(log_data)
    }
    logs_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[log_event])

@app.post('/')
async def main(json_body: dict):
    log_group_name = json_body['inputs']['log_group_name']
    log_stream_name = json_body['inputs']['log_stream_name']
    server_address = json_body['inputs']['server_address']
    request_data = json_body['inputs']['request_data']
    result, network_latency_time = predict(server_address, request_data)
    create_log_event(log_group_name, log_stream_name, result['inference_time'], network_latency_time)
    return "Success"