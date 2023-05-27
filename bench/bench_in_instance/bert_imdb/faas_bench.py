#preprocessing library
from bert_imdb import preprocessing
import numpy as np

#REST 요청 관련 library
from module import module_faas
import json

#병렬처리 library
import concurrent.futures

def run_bench(num_tasks, server_address):
    text = "This is a sample sentence to test the BERT model."
    input_ids, input_masks, segment_ids = preprocessing.run_preprocessing(text)

    data = json.dumps({"inputs": { "segment_ids": segment_ids, "input_masks": input_masks, "input_ids": input_ids.tolist()}})

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
