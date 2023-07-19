import time
cold_start_begin = time.time()
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import subprocess
import multiprocessing
from concurrent import futures
import grpc
import numpy as np
from tensorflow import make_ndarray
from tensorflow import make_tensor_proto
from tensorflow.keras.models import load_model
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import json
import requests

class PredictionServiceServicer(prediction_service_pb2_grpc.PredictionServiceServicer):
    def __init__(self):
        global model_load_end_time
        global model_load_start_time
        model_load_start_time = time.time()
        self.model = load_model('./bert_imdb')
        model_load_end_time = time.time()

    def Predict(self, request, context):
        execution_start_time = time.time()
        input_ids = make_ndarray(request.inputs["input_ids"])
        input_masks = make_ndarray(request.inputs["input_ids"])
        segment_ids = make_ndarray(request.inputs["segment_ids"])
        inference_start_time = time.time()
        model_output = self.model.predict([input_masks, input_ids, segment_ids])
        inference_end_time = time.time()
        response = predict_pb2.PredictResponse()
        response.outputs["output"].CopyFrom(make_tensor_proto(model_output, shape=list(model_output.shape)))
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
        cold_start_time_numpy = np.array((cold_start_end - cold_start_begin))
        inference_time_numpy = np.array((inference_end_time - inference_start_time))
        model_load_time_numpy = np.array((model_load_end_time - model_load_start_time))
        mem_bytes_numpy = np.array(mem_bytes)
        mem_gib_numpy = np.array(mem_gib)
        num_cores_numpy = np.array(num_cores)
        cpu_info_numpy = np.array(json.dumps(cpu_info).encode('utf-8'))
        mem_info_numpy = np.array(json.dumps(mem_info).encode('utf-8'))
        metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/id"
        metadata_headers = {'Metadata-Flavor': 'Google'}
        container_instance_id = requests.get(metadata_url, headers=metadata_headers)
        string_container_instance_id = container_instance_id.text
        container_instance_id_numpy = np.array(string_container_instance_id)
        response.outputs["inference_time"].CopyFrom(make_tensor_proto(inference_time_numpy, shape=list(inference_time_numpy.shape)))
        response.outputs["model_load_time"].CopyFrom(make_tensor_proto(model_load_time_numpy, shape=list(model_load_time_numpy.shape)))
        response.outputs["cold_start_time"].CopyFrom(make_tensor_proto(cold_start_time_numpy, shape=list(cold_start_time_numpy.shape)))
        response.outputs["mem_bytes"].CopyFrom(make_tensor_proto(mem_bytes_numpy, shape=list(mem_bytes_numpy.shape)))
        response.outputs["mem_gib"].CopyFrom(make_tensor_proto(mem_gib_numpy, shape=list(mem_gib_numpy.shape)))
        response.outputs["num_cores"].CopyFrom(make_tensor_proto(num_cores_numpy, shape=list(num_cores_numpy.shape)))
        response.outputs["cpu_info"].CopyFrom(make_tensor_proto(cpu_info_numpy, shape=list(cpu_info_numpy.shape)))
        response.outputs["mem_info"].CopyFrom(make_tensor_proto(mem_info_numpy, shape=list(mem_info_numpy.shape)))
        response.outputs["container_instance_id"].CopyFrom(make_tensor_proto(container_instance_id_numpy, shape=list(container_instance_id_numpy.shape)))
        execution_end_time = time.time()
        execution_start_time_numpy = np.array(execution_start_time)
        execution_end_time_numpy = np.array(execution_end_time)
        execution_time_numpy = np.array((execution_end_time - execution_start_time))
        response.outputs["execution_start_time"].CopyFrom(make_tensor_proto(execution_start_time_numpy, shape=list(execution_start_time_numpy.shape)))
        response.outputs["execution_end_time"].CopyFrom(make_tensor_proto(execution_end_time_numpy, shape=list(execution_end_time_numpy.shape)))
        response.outputs["execution_time"].CopyFrom(make_tensor_proto(execution_time_numpy, shape=list(execution_time_numpy.shape)))
        return response

def serve():
    print("Starting grpc server...")
    server_options = [
        ('grpc.max_send_message_length', 50*1024*1024),
        ('grpc.max_receive_message_length', 50*1024*1024)
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000), options=server_options)
    prediction_service_pb2_grpc.add_PredictionServiceServicer_to_server(PredictionServiceServicer(), server)
    server.add_insecure_port('[::]:8500')
    global cold_start_end
    cold_start_end = time.time()
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
