import json
import requests
import boto3
import time

logs_client = boto3.client('logs')

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
    log_data = {
        'inference_time': inference_time,
        'network_latency_time': network_latency_time
    }
    log_event = {
        'timestamp':int (time.time() * 1000),
        'message': json.dumps(log_data)
    }
    logs_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[log_event])

def lambda_handler(event,context):
    json_body = json.loads(event['body'])
    log_group_name = json_body['inputs']['log_group_name']
    log_stream_name = json_body['inputs']['log_stream_name']
    server_address = json_body['inputs']['server_address']
    request_data = json_body['inputs']['request_data']
    result, network_latency_time = predict(server_address, request_data)
    create_log_event(log_group_name, log_stream_name, result['inference_time'], network_latency_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response