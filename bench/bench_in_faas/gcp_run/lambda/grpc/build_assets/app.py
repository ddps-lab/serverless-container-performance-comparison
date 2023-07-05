import json
import boto3
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from google.protobuf.json_format import ParseDict
import grpc

def create_grpc_stub(server_address, use_https):
    # gRPC 채널 생성
    if (use_https == "1"):
        channel = grpc.secure_channel(server_address,grpc.ssl_channel_credentials(),options=[('grpc.max_send_message_length', 50 * 1024 * 1024), ('grpc.max_receive_message_length', 50 * 1024 * 1024)])
    else:
        channel = grpc.insecure_channel(server_address,options=[('grpc.max_send_message_length', 50 * 1024 * 1024), ('grpc.max_receive_message_length', 50 * 1024 * 1024)])

    # gRPC 스텁 생성
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    return stub

def predict(stub, data):
    request_time = time.time()
    response = stub.Predict(data, timeout=100.0)
    response_time = time.time()
    start_time = response.outputs['start_time'].double_val[0]
    network_latency_time = response_time - request_time
    return response, start_time, network_latency_time

def create_log_event(log_group_name, log_stream_name, start_latency_time, response, network_latency_time, bench_execute_latency_time):
    logs_client = boto3.client('logs')
    container_instance_id = (response.outputs['container_instance_id'].string_val[0]).decode('utf-8')
    log_data = {
        'container_instance_id': container_instance_id[-20:],
        'bench_execute_latency_time': bench_execute_latency_time,
        'start_latency_time': start_latency_time,
        'inference_time': response.outputs['inference_time'].double_val[0],
        'network_latency_time': network_latency_time,
        'cpu_info': json.loads(response.outputs['cpu_info'].string_val[0]),
        'mem_info': json.loads(response.outputs['mem_info'].string_val[0]),
        'num_cores': response.outputs['num_cores'].int64_val[0],
        'mem_bytes': response.outputs['mem_bytes'].int64_val[0],
        'mem_gib': response.outputs['mem_gib'].double_val[0],
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
    use_https = json_body['inputs']['use_https']
    request_data = json_body['inputs']['request_data']
    bench_execute_request_time = json_body['inputs']['bench_execute_request_time']
    protobuf_message = predict_pb2.PredictRequest()
    ParseDict(json.loads(request_data), protobuf_message)
    request_time = time.time()
    stub = create_grpc_stub(server_address, use_https)
    response, start_time, network_latency_time = predict(stub, protobuf_message)
    create_log_event(log_group_name, log_stream_name, start_time - request_time, response, network_latency_time, bench_execute_time - bench_execute_request_time)
    response = {
        'statusCode': 200,
        'body': "Success"
    }
    return response