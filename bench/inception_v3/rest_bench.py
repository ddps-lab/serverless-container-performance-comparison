#preprocessing library
from inception_v3 import preprocessing
import numpy as np

#REST 요청 관련 library
from module import module_rest
import json

#병렬처리 library
import concurrent.futures

def run_bench(num_tasks, server_address):
    model_name = "inception_v3"
    image_file_path = "../../../dataset/imagenet/imagenet_1000_raw/n01843383_1.JPEG"
    
    data = json.dumps({"instances": preprocessing.run_preprocessing(image_file_path).tolist()})

    # REST 요청 병렬 처리
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
        futures = [executor.submit(lambda: module_rest.predict(server_address, model_name, data)) for _ in range(num_tasks)]

    inference_times_include_network_latency = []
    for future in concurrent.futures.as_completed(futures):
        result, thread_elapsed_time = future.result()
        inference_times_include_network_latency.append(thread_elapsed_time)

    return inference_times_include_network_latency
