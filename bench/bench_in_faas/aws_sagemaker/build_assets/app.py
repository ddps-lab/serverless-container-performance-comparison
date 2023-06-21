import json
import requests
import boto3
import time
from sagemaker import Session
from sagemaker.predictor import Predictor

def predict(sagemaker_endpoint, data):
    session = Session()
    predictor = Predictor(endpoint_name=sagemaker_endpoint, sagemaker_session=session)    
    request_time = time.time()
    response = predictor.predict(data)
    response_time = time.time()
    network_latency_time = response_time - request_time
    return response, network_latency_time

def create_log_event(log_group_name, log_stream_name, result, network_latency_time):
    result_json = json.loads(result)
    logs_client = boto3.client('logs')
    log_data = {
        'inference_time': result['inference_time'],
        'network_latency_time': network_latency_time,
        'cpu_info': result['cpu_info'],
        'mem_info': result['mem_info'],
        'num_cores': result['num_cores'],
        'mem_bytes': result['mem_bytes'],
        'mem_gib': result['mem_gib']
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
    sagemaker_endpoint = f"{aws_sagemaker_endpoint_prefix}-{model_name.replace('_','-')}-endpoint"
    result, network_latency_time = predict(sagemaker_endpoint, request_data)
    create_log_event(log_group_name, log_stream_name, result, network_latency_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response