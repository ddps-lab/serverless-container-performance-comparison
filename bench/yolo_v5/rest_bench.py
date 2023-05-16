import boto3
#preprocessing library
from yolo_v5 import preprocessing
import numpy as np

#REST 요청 관련 library
from module import module_rest
import json

import time

#병렬처리 library
import concurrent.futures

def run_bench(num_tasks, server_address, using_lambda=0, bucket_name=''):
    model_name = "yolo_v5"
    image_file_path = "../../dataset/coco_2017/coco/images/val2017/000000000139.jpg"
    
    if (using_lambda == 1):
        np.save('preprocessed_data', preprocessing.run_preprocessing(image_file_path))
        s3 = boto3.resource('s3')
        upload_start_time = time.time()
        s3.Bucket(bucket_name).upload_file('./preprocessed_data.npy', "preprocessed_data.npy")
        upload_time = time.time() - upload_start_time
        data = json.dumps({"inputs": {"s3_bucket_name": bucket_name, "s3_object_name": "preprocessed_data.npy"}})
        # REST 요청 병렬 처리
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
            futures = [executor.submit(lambda: module_rest.predict(server_address, model_name, data, using_lambda=using_lambda)) for _ in range(num_tasks)]

        inference_times_include_network_latency = []
        for future in concurrent.futures.as_completed(futures):
            result, thread_elapsed_time = future.result()
            download_start_time = time.time()
            s3.Bucket(bucket_name).download_file("predict_data.npy", "./tmp_file")
            download_time = time.time() - download_start_time
            inference_times_include_network_latency.append(thread_elapsed_time+upload_time+download_time)

        return inference_times_include_network_latency
    else:
        data = json.dumps({"inputs": {"x": preprocessing.run_preprocessing(image_file_path).tolist()}})
        
        # REST 요청 병렬 처리
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
            futures = [executor.submit(lambda: module_rest.predict(server_address, model_name, data)) for _ in range(num_tasks)]

        inference_times_include_network_latency = []
        for future in concurrent.futures.as_completed(futures):
            result, thread_elapsed_time = future.result()
            inference_times_include_network_latency.append(thread_elapsed_time)

        return inference_times_include_network_latency
