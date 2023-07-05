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
    result = response.json()
    return result, network_latency_time

def create_log_event(log_group_name, log_stream_name, start_latency_time, result, network_latency_time, bench_execute_latency_time):
    logs_client = boto3.client('logs')
    log_data = {
        'container_instance_id': (result['container_instance_id'])[-20:],
        'bench_execute_latency_time': bench_execute_latency_time,
        'start_latency_time': start_latency_time,
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
    bench_execute_time = time.time()
    json_body = json.loads(event['body'])
    log_group_name = json_body['inputs']['log_group_name']
    log_stream_name = json_body['inputs']['log_stream_name']
    server_address = json_body['inputs']['server_address']
    request_data = json_body['inputs']['request_data']
    bench_execute_request_time = json_body['inputs']['bench_execute_request_time']
    request_time = time.time()
    result, network_latency_time = predict(server_address, request_data)
    create_log_event(log_group_name, log_stream_name, result['start_time'] - request_time, result, network_latency_time, bench_execute_time - bench_execute_request_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response