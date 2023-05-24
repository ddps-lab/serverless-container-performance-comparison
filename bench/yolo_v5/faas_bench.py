import boto3
from azure.storage.blob import BlobServiceClient
from pathlib import Path
#preprocessing library
from yolo_v5 import preprocessing
import numpy as np

#REST 요청 관련 library
from module import module_faas
import json

import time

#병렬처리 library
import concurrent.futures

def run_bench(num_tasks, server_address, service_name='', bucket_name='', blob_connection_string='', blob_container_name=''):
    image_file_path = "../../dataset/coco_2017/coco/images/val2017/000000000139.jpg"
    
    if (service_name == "aws_lambda"):
        np.save('preprocessed_data', preprocessing.run_preprocessing(image_file_path))
        s3 = boto3.resource('s3')
        upload_start_time = time.time()
        s3.Bucket(bucket_name).upload_file('./preprocessed_data.npy', "preprocessed_data.npy")
        upload_time = time.time() - upload_start_time
        data = json.dumps({"inputs": {"s3_bucket_name": bucket_name, "s3_object_name": "preprocessed_data.npy"}})
        # REST 요청 병렬 처리
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
            futures = [executor.submit(lambda: module_faas.predict(server_address, data)) for _ in range(num_tasks)]

        inference_times = []
        network_latency_times = []
        for future in concurrent.futures.as_completed(futures):
            result, thread_elapsed_time = future.result()
            download_start_time = time.time()
            s3.Bucket(bucket_name).download_file("predict_data.npy", "./tmp_file")
            download_time = time.time() - download_start_time
            inference_times.append(result['inference_time'])
            network_latency_times.append(thread_elapsed_time+upload_time+download_time)

        return inference_times, network_latency_times
    
    elif (service_name == 'azure_function'):
        np.save('preprocessed_data', preprocessing.run_preprocessing(image_file_path))
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        container_client = blob_service_client.get_container_client(blob_container_name)
        upload_start_time = time.time()
        with open("./preprocessed_data.npy", "rb") as data:
            container_client.upload_blob(name="preprocessed_data.npy", data=data, overwrite=True)
        upload_time = time.time() - upload_start_time
        data = json.dumps({"inputs": {"blob_container_name": blob_container_name, "blob_name": "preprocessed_data.npy"}})
        # REST 요청 병렬 처리
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
            futures = [executor.submit(lambda: module_faas.predict(server_address, data)) for _ in range(num_tasks)]

        inference_times = []
        network_latency_times = []
        for future in concurrent.futures.as_completed(futures):
            result, thread_elapsed_time = future.result()
            download_start_time = time.time()
            with open("./tmp_file", "wb") as file:
                blob_client = container_client.get_blob_client("predict_data.npy")
                blob_data = blob_client.download_blob()
                blob_data.readinto(file)
            download_time = time.time() - download_start_time
            inference_times.append(result['inference_time'])
            network_latency_times.append(thread_elapsed_time+upload_time+download_time)

        return inference_times, network_latency_times
    else:
        data = json.dumps({"inputs": {"x": preprocessing.run_preprocessing(image_file_path).tolist()}})
        
        # REST 요청 병렬 처리
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
            futures = [executor.submit(lambda: module_faas.predict(server_address, data)) for _ in range(num_tasks)]

        inference_times = []
        network_latency_times = []
        for future in concurrent.futures.as_completed(futures):
            result, thread_elapsed_time = future.result()
            inference_times.append(result['inference_time'])
            network_latency_times.append(thread_elapsed_time)

        return inference_times, network_latency_times
