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

def create_log_event(log_group_name, log_stream_name, request_time, result, network_latency_time, bench_execute_latency_time):
    result_json = json.loads(result)
    logs_client = boto3.client('logs')
    log_data = {
        'bench_execute_latency_time': bench_execute_latency_time,
        'start_latency_time': result_json['start_time'] - request_time,
        'inference_time': result_json['inference_time'],
        'network_latency_time': network_latency_time,
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
    # aws_region = json_body['inputs']['aws_region']
    model_name = json_body['inputs']['model_name']
    log_group_name = json_body['inputs']['log_group_name']
    log_stream_name = json_body['inputs']['log_stream_name']
    aws_sagemaker_endpoint_prefix = json_body['inputs']['sagemaker_endpoint_prefix']
    # request_data = json_body['inputs']['request_data']
    # upload_time = json_body['inputs']['upload_time']
    # bucket_name = json_body['inputs']['bucket_name']
    bench_execute_request_time = json_body['inputs']['bench_execute_request_time']
    with open(f"./{model_name}.json", "r", encoding="utf-8") as f:
        request_data = json.dumps(json.load(f))
    sagemaker_endpoint = f"{aws_sagemaker_endpoint_prefix}-{model_name.replace('_','-')}-endpoint"
    request_time = time.time()
    # result, network_latency_time = predict(sagemaker_endpoint, request_data, bucket_name)
    result, network_latency_time = predict(sagemaker_endpoint, request_data)
    # download_time = 0
    # if (model_name == "yolo_v5" or model_name == "inception_v3"):
    #     s3_resource = boto3.resource('s3')
    #     download_start_time = time.time()
    #     s3_resource.Bucket(bucket_name).download_file("predict_data.npy", "/tmp/tmp_file")
    #     download_time = time.time() - download_start_time
    # create_log_event(log_group_name, log_stream_name, request_time, result, upload_time+network_latency_time+download_time, bench_execute_time - bench_execute_request_time)
    create_log_event(log_group_name, log_stream_name, request_time, result, network_latency_time, bench_execute_time - bench_execute_request_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response