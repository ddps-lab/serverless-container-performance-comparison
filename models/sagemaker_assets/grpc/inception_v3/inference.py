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
import requests

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
    http_body_bytes = data.read()
    http_body_str = http_body_bytes.decode('utf-8')
    json_body = json.loads(http_body_str)
    get_url = json_body['inputs']['get_url']
    put_url = json_body['inputs']['put_url']
    protobuf_message = predict_pb2.PredictRequest()
    stub = create_grpc_stub(f"0.0.0.0:{context.grpc_port}")
    request_data = requests.get(get_url)
    ParseDict(json.loads(request_data.content), protobuf_message)
    response, inference_time = predict(stub, protobuf_message)
    requests.put(put_url, data=response.SerializeToString())
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
    response_json = {
        "cold_start_time": cold_start_end - cold_start_begin,
        "execution_start_time": execution_start_time,
        "execution_end_time": execution_end_time,
        "execution_time": execution_end_time - execution_start_time,
        "inference_time": inference_time,
        "mem_bytes": mem_bytes,
        "mem_gib": mem_gib,
        "num_cores": num_cores,
        "cpu_info": cpu_info,
        "mem_info": mem_info
    }
    result = json.dumps(response_json).encode('utf-8')
    return result, context.accept_header