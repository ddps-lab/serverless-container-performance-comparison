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
    inference_start_time = time.time()
    response = requests.post(context.rest_uri, data=data)
    inference_end_time = time.time()
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
    response_json = json.loads(response.content)
    response_json['cold_start_time'] = cold_start_end - cold_start_begin
    response_json['execution_start_time'] = execution_start_time
    response_json['execution_end_time'] = execution_end_time
    response_json['execution_time'] = execution_end_time - execution_start_time
    response_json['inference_time'] = inference_end_time - inference_start_time
    response_json['mem_bytes'] = mem_bytes
    response_json['mem_gib'] = mem_gib
    response_json['num_cores'] = num_cores
    response_json['cpu_info'] = cpu_info
    response_json['mem_info'] = mem_info
    result = json.dumps(response_json).encode('utf-8')
    return result, context.accept_header