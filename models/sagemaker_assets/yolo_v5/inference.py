import json
import time
from collections import namedtuple
import requests
import os
import subprocess
import multiprocessing
import numpy as np

Context = namedtuple('Context',
                     'model_name, model_version, method, rest_uri, grpc_uri, '
                     'custom_attributes, request_content_type, accept_header')

def handler(data, context):
    http_body_bytes = data.read()
    http_body_str = http_body_bytes.decode('utf-8')
    json_body = json.loads(http_body_str)
    s3_bucket_name = json_body['inputs']['s3_bucket_name']
    s3_object_name = json_body['inputs']['s3_object_name']
    start_time = time.time()
    subprocess.call(f"/usr/local/bin/aws s3 cp s3://{s3_bucket_name}/{s3_object_name} /tmp/preprocessed_data.npy", shell=True)
    print("download")
    data = json.dumps({"inputs": { "x": np.load("/tmp/preprocessed_data.npy").tolist()}})
    response = requests.post(context.rest_uri, data=data)
    print("response")
    with open("/tmp/predict_data.npy", "wb") as f:
        f.write(response.content)
    print("create file")
    subprocess.call(f"/usr/local/bin/aws s3 cp /tmp/predict_data.npy s3://{s3_bucket_name}/predict_data.npy", shell=True)
    print("upload")
    end_time = time.time()
    inference_time = end_time - start_time
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
    response_json = {
        "inference_time": inference_time,
        "mem_bytes": mem_bytes,
        "mem_gib": mem_gib,
        "num_cores": num_cores,
        "cpu_info": cpu_info,
        "mem_info": mem_info
    }
    result = json.dumps(response_json).encode('utf-8')
    return result, context.accept_header