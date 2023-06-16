import json
import requests
import boto3
import time

def predict(server_address, data):
    headers = {"content-type": "application/json"}
    url = server_address
    request_time = time.time()
    response = requests.post(url, data=data, headers=headers)
    response_time = time.time()
    network_latency_time = response_time - request_time
    result = response.text
    return result, network_latency_time

def create_log_event(log_group_name, log_stream_name, network_latency_time):
    logs_client = boto3.client('logs')
    log_data = {
        'network_latency_time': network_latency_time
    }
    log_event = {
        'timestamp':int (time.time() * 1000),
        'message': json.dumps(log_data)
    }
    logs_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[log_event])

def lambda_handler(event,context):
    json_body = json.loads(event['body'])
    aws_region = json_body['inputs']['aws_region']
    model_name = json_body['inputs']['model_name']
    log_group_name = json_body['inputs']['log_group_name']
    log_stream_name = json_body['inputs']['log_stream_name']
    aws_sagemaker_endpoint_prefix = json_body['inputs']['sagemaker_endpoint_prefix']
    request_data = json_body['inputs']['request_data']
    server_address = f"https://runtime.sagemaker.{aws_region}.amazonaws.com/endpoints/{aws_sagemaker_endpoint_prefix}-{model_name.replace('_','-')}-endpoint/invocations"
    result, network_latency_time = predict(server_address, request_data)
    create_log_event(log_group_name, log_stream_name, network_latency_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response