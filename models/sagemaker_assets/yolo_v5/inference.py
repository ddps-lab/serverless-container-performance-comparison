import time
global cold_start_begin
global cold_start_end
cold_start_begin = time.time()
import json
from collections import namedtuple
import requests
import os
import subprocess
import multiprocessing

Context = namedtuple('Context',
                     'model_name, model_version, method, rest_uri, grpc_uri, '
                     'custom_attributes, request_content_type, accept_header')

cold_start_end = time.time()

def handler(data, context):
    execution_start_time = time.time()
    http_body_bytes = data.read()
    http_body_str = http_body_bytes.decode('utf-8')
    json_body = json.loads(http_body_str)
    s3_bucket_name = json_body['inputs']['s3_bucket_name']
    s3_preprocessed_data_key_path = json_body['inputs']['s3_preprocessed_data_key_path']
    subprocess.call(f"/usr/local/bin/aws s3 cp s3://{s3_bucket_name}/{s3_preprocessed_data_key_path}yolo_v5.json /tmp/preprocessed_data.json", shell=True)
    with open("/tmp/preprocessed_data.json", "r") as f:
        inference_start_time = time.time()
        response = requests.post(context.rest_uri, data=json.load(f))
    inference_end_time = time.time()
    with open("/tmp/predict_data.npy", "wb") as f:
        f.write(response.content)
    subprocess.call(f"/usr/local/bin/aws s3 cp /tmp/predict_data.npy s3://{s3_bucket_name}/predict_data.npy", shell=True)
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
        "inference_time": inference_end_time - inference_start_time,
        "mem_bytes": mem_bytes,
        "mem_gib": mem_gib,
        "num_cores": num_cores,
        "cpu_info": cpu_info,
        "mem_info": mem_info
    }
    result = json.dumps(response_json).encode('utf-8')
    return result, context.accept_header