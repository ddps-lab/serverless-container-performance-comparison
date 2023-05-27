#preprocessing library
from distilbert_sst2 import preprocessing
import numpy as np

#REST 요청 관련 library
from module import module_rest
import json

#병렬처리 library
import concurrent.futures

def run_bench(num_tasks, server_address):
    model_name = "distilbert_sst2"
    
    text = "This is a sample sentence to test the BERT model."
    bert_input_ids, bert_input_masks = preprocessing.run_preprocessing(text)

    data = json.dumps({"inputs": { "bert_input_masks": bert_input_masks, "bert_input_ids": bert_input_ids.tolist()}})

    # REST 요청 병렬 처리
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_tasks) as executor:
        futures = [executor.submit(lambda: module_rest.predict(server_address, model_name, data)) for _ in range(num_tasks)]

    inference_times_include_network_latency = []
    for future in concurrent.futures.as_completed(futures):
        result, thread_elapsed_time = future.result()
        inference_times_include_network_latency.append(thread_elapsed_time)

    return inference_times_include_network_latency
