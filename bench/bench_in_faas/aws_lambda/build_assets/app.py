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

def create_log_event(log_group_name, log_stream_name, inference_time, network_latency_time):
    logs_client = boto3.client('logs')
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
    model_name = json_body['inputs']['model_name']
    log_group_name = json_body['inputs']['log_group_name']
    log_stream_name = json_body['inputs']['log_stream_name']
    server_address = json_body['inputs']['server_address']
    data = json_body['inputs']['request_data']
    bucket_name = json_body['inputs']['bucket_name']
    upload_time = int(json_body['inputs']['upload_time'])
    download_time = 0
    request_data = data[0]
    result, network_latency_time = predict(server_address, request_data)
    if (model_name == "yolo_v5"):
        s3_resource = boto3.resource('s3')
        download_start_time = time.time()
        s3_resource.Bucket(bucket_name).download_file("predict_data.npy", "/tmp_file")
        download_time = time.time() - download_start_time
    create_log_event(log_group_name, log_stream_name, result['inference_time'], upload_time+network_latency_time+download_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response