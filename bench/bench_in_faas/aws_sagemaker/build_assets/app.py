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

def create_log_event(model_name, log_group_name, log_stream_name, request_time, to_start_request_latency_time, result, network_latency_time, bench_execute_latency_time):
    result_json = json.loads(result)
    logs_client = boto3.client('logs')
    log_data = {
        'bench_execute_latency_time': bench_execute_latency_time,
        'to_start_request_latency_time': to_start_request_latency_time,
        'start_latency_time': result_json['execution_start_time'] - request_time,
        'inference_time': result_json['inference_time'],
        'network_latency_time': network_latency_time,
        'cold_start_time': result_json['cold_start_time'],
        'execution_start_time': result_json['execution_start_time'],
        'execution_end_time': result_json['execution_end_time'],
        'execution_time': result_json['execution_time'],
        'cpu_info': result_json['cpu_info'],
        'mem_info': result_json['mem_info'],
        'num_cores': result_json['num_cores'],
        'mem_bytes': result_json['mem_bytes'],
        'mem_gib': result_json['mem_gib']
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
    s3_bucket_name = json_body['inputs']['s3_bucket_name']
    s3_preprocessed_data_key_path = json_body['inputs']['s3_preprocessed_data_key_path']
    aws_sagemaker_endpoint_prefix = json_body['inputs']['sagemaker_endpoint_prefix']
    bench_execute_request_time = json_body['inputs']['bench_execute_request_time']
    tfserving_protocol = json_body['inputs']['tfserving_protocol']
    if (model_name == "yolo_v5" or model_name == "inception_v3"):
        request_data = json.dumps({"inputs": {"s3_bucket_name": s3_bucket_name, "s3_preprocessed_data_key_path": s3_preprocessed_data_key_path}})
    else:
        with open(f"./{model_name}-{tfserving_protocol}.json", "r", encoding="utf-8") as f:
            request_data = json.dumps(json.load(f))
    sagemaker_endpoint = f"{aws_sagemaker_endpoint_prefix}-{model_name.replace('_','-')}-endpoint"
    request_time = time.time()
    result, network_latency_time = predict(sagemaker_endpoint, request_data)
    create_log_event(model_name, log_group_name, log_stream_name, request_time, request_time - bench_execute_time, result, network_latency_time, bench_execute_time - bench_execute_request_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response