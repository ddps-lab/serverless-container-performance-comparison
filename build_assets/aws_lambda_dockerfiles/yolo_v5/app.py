import json
import boto3
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import subprocess
import multiprocessing
import time
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model('./yolo_v5')
model_load_end_time = time.time()

def lambda_handler(event,context):
    start_time = time.time()
    json_body = json.loads(event['body'])
    s3_bucket_name = json_body['inputs']['s3_bucket_name']
    s3_object_name = json_body['inputs']['s3_object_name']
    s3 = boto3.resource('s3')
    s3.Bucket(s3_bucket_name).download_file(s3_object_name, "/tmp/preprocessed_data.npy")
    result = model(np.load("/tmp/preprocessed_data.npy"))
    np.save('/tmp/predict_data', result)
    s3.Bucket(s3_bucket_name).upload_file("/tmp/predict_data.npy", "predict_data.npy")
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
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'start_time': start_time,
            'loading_time': model_load_end_time - model_load_start_time,
            'inference_time': end_time - start_time,
            'mem_bytes': mem_bytes,
            'mem_gib': mem_gib,
            'num_cores': num_cores,
            'cpu_info': cpu_info,
            'mem_info': mem_info,
            'body': "S3 Uploaded"
        })
    }
    return response