import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import subprocess
import multiprocessing
import numpy as np
import time
import requests
from fastapi import FastAPI
app = FastAPI()
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model('./mobilenet_v1')
model_load_end_time = time.time()

@app.post('/')
async def predict(json_body: dict):
    start_time = time.time()
    input_1 = json_body['inputs']['input_1']
    result = model.predict(np.array(input_1))
    end_time = time.time()
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
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/id"
    metadata_headers = {'Metadata-Flavor': 'Google'}
    container_instance_id = requests.get(metadata_url, headers=metadata_headers)
    string_container_instance_id = container_instance_id.text
    response = {
        'start_time': start_time,
        'loading_time': model_load_end_time - model_load_start_time,
        'inference_time': end_time - start_time,
        'mem_bytes': mem_bytes,
        'mem_gib': mem_gib,
        'num_cores': num_cores,
        'cpu_info': cpu_info,
        'mem_info': mem_info,
        'container_instance_id': string_container_instance_id,
        'body': result.tolist(),
    }
    return response