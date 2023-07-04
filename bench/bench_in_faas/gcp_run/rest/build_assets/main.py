import functions_framework
import json
import requests
import boto3
import time
import os

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

def create_log_event(log_group_name, log_stream_name, start_latency_time, result, network_latency_time, bench_execute_latency_time):
    logs_client = boto3.client('logs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
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

@functions_framework.http
def function_handler(request):
    if request.method == 'POST':
        bench_execute_time = time.time()
        json_body = request.get_json(silent=True)
        log_group_name = json_body['inputs']['log_group_name']
        log_stream_name = json_body['inputs']['log_stream_name']
        server_address = json_body['inputs']['server_address']
        request_data = json_body['inputs']['request_data']
        bench_execute_request_time = json_body['inputs']['bench_execute_request_time']
        request_time = time.time()
        result, network_latency_time = predict(server_address, request_data)
        create_log_event(log_group_name, log_stream_name, request_time - result['start_time'], result, network_latency_time, bench_execute_time - bench_execute_request_time)
        return json.dumps({'body': "Success"}), 200, {'Content-Type': 'application/json'}
    else:
        return json.dumps({
            'body': "Please send POST request"
        }), 403, {'Content-Type': 'application/json'}