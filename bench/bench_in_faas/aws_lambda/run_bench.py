import json
import time
import concurrent.futures
import variables
import requests
import boto3
import importlib

logs_client = boto3.client('logs')
faas_bench = ""

def create_log_stream(log_group_name, log_stream_name):
    logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

def request_predict(server_address, data):
    headers = {"content-type": "application/json"}
    url = f"https://{server_address}/"
    response = requests.post(url, data=data, headers=headers)
    result = response.text
    return result

def start_bench(model_names, num_tasks, aws_lambda_address, aws_lambda_default_address, bucket_name, log_group_name):
  for i, model_name in enumerate(model_names):
    global faas_bench
    faas_bench = importlib.import_module(f"preprocess.{model_name}")
    request_data, upload_time = faas_bench.create_request_data(bucket_name)
    for k, num_task in enumerate(num_tasks):
      current_timestamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
      log_stream_name = f"{current_timestamp}-{model_name}-{num_task}tasks"
      bench_execute_request_time = time.time()
      data = json.dumps({
         "inputs": {
            "bench_execute_request_time": bench_execute_request_time,
            "model_name": model_name,
            "request_data": request_data,
            "log_group_name": log_group_name,
            "log_stream_name": log_stream_name,
            "server_address":  f"https://{model_name.replace('_','-')}.{aws_lambda_default_address}/",
            "bucket_name": bucket_name,
            "upload_time": upload_time
         }
      })
      create_log_stream(log_group_name, log_stream_name)
      with concurrent.futures.ThreadPoolExecutor(max_workers=num_task) as executor:
        futures = [executor.submit(lambda: request_predict(aws_lambda_address, data)) for _ in range(num_task)]
      for future in concurrent.futures.as_completed(futures):
        result = future.result()
      time.sleep(5)

start_bench(variables.model_names,
            variables.num_tasks,
            variables.aws_lambda_address,
            variables.aws_lambda_default_address,
            variables.bucket_name,
            variables.log_group_name)