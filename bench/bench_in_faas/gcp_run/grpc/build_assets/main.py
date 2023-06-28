import functions_framework
import json
import boto3
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from google.protobuf.json_format import ParseDict
import grpc

aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
aws_region = os.environ['AWS_REGION']

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

def create_log_event(log_group_name, log_stream_name, start_latency_time, response, network_latency_time):
    logs_client = boto3.client('logs', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)
    log_data = {
        'start_latency_time': start_latency_time,
        'inference_time': response.outputs['inference_time'].double_val[0],
        'network_latency_time': network_latency_time,
        'cpu_info': json.loads(response.outputs['cpu_info'].string_val[0]),
        'mem_info': json.loads(response.outputs['mem_info'].string_val[0]),
        'num_cores': response.outputs['num_cores'].int64_val[0],
        'mem_bytes': response.outputs['mem_bytes'].int64_val[0],
        'mem_gib': response.outputs['mem_gib'].double_val[0]
    }
    log_event = {
        'timestamp':int (time.time() * 1000),
        'message': json.dumps(log_data)
    }
    logs_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, logEvents=[log_event])

@functions_framework.http
def function_handler(request):
    if request.method == 'POST':
        json_body = request.get_json(silent=True)
        log_group_name = json_body['inputs']['log_group_name']
        log_stream_name = json_body['inputs']['log_stream_name']
        server_address = json_body['inputs']['server_address']
        use_https = json_body['inputs']['use_https']
        request_data = json_body['inputs']['request_data']
        protobuf_message = predict_pb2.PredictRequest()
        ParseDict(json.loads(request_data), protobuf_message)
        request_time = time.time()
        stub = create_grpc_stub(server_address, use_https)
        response, start_time, network_latency_time = predict(stub, protobuf_message)
        create_log_event(log_group_name, log_stream_name, start_time - request_time, response, network_latency_time)
        return json.dumps({'body': "Success"}), 200, {'Content-Type': 'application/json'}
    else:
        return json.dumps({
            'body': "Please send POST request"
        }), 403, {'Content-Type': 'application/json'}