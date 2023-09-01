import time
global cold_start_begin
global cold_start_end
cold_start_begin = time.time()
import json
from collections import namedtuple
import os
import subprocess
import multiprocessing
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
from google.protobuf.json_format import ParseDict
from google.protobuf.json_format import MessageToDict
import grpc

Context = namedtuple('Context',
                     'model_name, model_version, method, rest_uri, grpc_uri, '
                     'custom_attributes, request_content_type, accept_header')

cold_start_end = time.time()

def create_grpc_stub(server_address):
    # gRPC 채널 생성
    channel = grpc.insecure_channel(server_address,options=[('grpc.max_send_message_length', 50 * 1024 * 1024), ('grpc.max_receive_message_length', 50 * 1024 * 1024)])

    # gRPC 스텁 생성
    stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
    return stub

def predict(stub, data):
    request_time = time.time()
    response = stub.Predict(data, timeout=100.0)
    response_time = time.time()
    inference_time = response_time - request_time
    return response, inference_time

def handler(data, context):
    execution_start_time = time.time()
    protobuf_message = predict_pb2.PredictRequest()
    ParseDict(json.loads(data.read().decode('utf-8')), protobuf_message)
    stub = create_grpc_stub(f"0.0.0.0:{context.grpc_port}")
    response, inference_time = predict(stub, protobuf_message)
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes/(1024.**3)
    num_cores = multiprocessing.cpu_count()
    cpu_info_cat = subprocess.run(['cat','/proc/cpuinfo'], capture_output=True, text=True)
    cpu_info_output = cpu_info_cat.stdout
    cpu_info = []
    current_cpu = {}
    for line in cpu_info_output.splitlines():
        if line.strip():
            key, value = line.split(':',1)
            current_cpu[key.strip()] = value.strip()
        else:
            cpu_info.append(current_cpu)
            current_cpu = {}
    cpu_info.append(current_cpu)
    mem_info_cat = subprocess.run(['cat','/proc/meminfo'], capture_output=True, text=True)
    mem_info_output = mem_info_cat.stdout
    mem_info = []
    current_mem = {}
    for line in mem_info_output.splitlines():
        if line.strip():
            key, value = line.split(':',1)
            current_mem[key.strip()] = value.strip()
        else:
            mem_info.append(current_mem)
            current_mem = {}
    mem_info.append(current_mem)
    execution_end_time = time.time()
    response_json = MessageToDict(response)
    response_json['cold_start_time'] = cold_start_end - cold_start_begin
    response_json['execution_start_time'] = execution_start_time
    response_json['execution_end_time'] = execution_end_time
    response_json['execution_time'] = execution_end_time - execution_start_time
    response_json['inference_time'] = inference_time
    response_json['mem_bytes'] = mem_bytes
    response_json['mem_gib'] = mem_gib
    response_json['num_cores'] = num_cores
    response_json['cpu_info'] = cpu_info
    response_json['mem_info'] = mem_info
    result = json.dumps(response_json).encode('utf-8')
    return result, context.accept_header