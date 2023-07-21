import time
global cold_start_begin
global cold_start_end
cold_start_begin = time.time()
import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import subprocess
import multiprocessing
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model('./inception_v3')
model_load_end_time = time.time()
cold_start_end = time.time()

def lambda_handler(event,context):
    execution_start_time = time.time()
    json_body = json.loads(event['body'])
    input_3 = json_body['inputs']['input_3']
    inference_start_time = time.time()
    result = model.predict(np.array(input_3))
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
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'cold_start_time': cold_start_end - cold_start_begin,
            'execution_start_time': execution_start_time,
            'execution_end_time': execution_end_time,
            'execution_time': execution_end_time - execution_start_time,
            'model_load_time': model_load_end_time - model_load_start_time,
            'inference_time': inference_end_time - inference_start_time,
            'mem_bytes': mem_bytes,
            'mem_gib': mem_gib,
            'num_cores': num_cores,
            'cpu_info': cpu_info,
            'mem_info': mem_info,
            'body': result.tolist(),
        })
    }
    return response