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

def create_log_event(model_name, log_group_name, log_stream_name, start_latency_time, to_start_request_latency_time, result, network_latency_time, bench_execute_latency_time):
    logs_client = boto3.client('logs')
    log_data = {
        'bench_execute_latency_time': bench_execute_latency_time,
        'to_start_request_latency_time': to_start_request_latency_time,
        'start_latency_time': start_latency_time,
        'inference_time': result['inference_time'],
        'network_latency_time': network_latency_time,
        'cold_start_time': result['cold_start_time'],
        'execution_start_time': result['execution_start_time'],
        'execution_end_time': result['execution_end_time'],
        'execution_time': result['execution_time'],
        'model_load_time': result['model_load_time'],
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
    model_name = json_body['inputs']['model_name']
    log_group_name = json_body['inputs']['log_group_name']
    log_stream_name = json_body['inputs']['log_stream_name']
    server_address = json_body['inputs']['server_address']
    s3_bucket_name = json_body['inputs']['s3_bucket_name']
    s3_preprocessed_data_key_path = json_body['inputs']['s3_preprocessed_data_key_path']
    bench_execute_request_time = json_body['inputs']['bench_execute_request_time']
    if (model_name == "yolo_v5"):
        request_data = json.dumps({"inputs": {"s3_bucket_name": s3_bucket_name, "s3_preprocessed_data_key_path": s3_preprocessed_data_key_path}})
    else:
        with open(f"./{model_name}.json", "r", encoding="utf-8") as f:
            request_data = json.dumps(json.load(f))
    request_time = time.time()
    result, network_latency_time = predict(server_address, request_data)
    create_log_event(model_name, log_group_name, log_stream_name, result['execution_start_time'] - request_time, request_time - bench_execute_time, result, network_latency_time, bench_execute_time - bench_execute_request_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response