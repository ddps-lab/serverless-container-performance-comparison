from module import put_data_into_sheet
from module import module_cw_logs
import importlib
faas_bench = ""

def main(model_name, num_tasks, server_address, spreadsheet_id, worksheet_name, service_name, bucket_name='', blob_connection_string='', blob_container_name='', log_group_name='', inference_time_log_stream_name='', network_latency_time_log_stream_name=''):
  global faas_bench
  faas_bench = importlib.import_module(f"{model_name}.faas_bench")
  if (model_name == "yolo_v5" and service_name == "aws_lambda"):
    inference_times, network_latency_times = faas_bench.run_bench(num_tasks, server_address, service_name, bucket_name=bucket_name)
  elif (model_name == "yolo_v5" and service_name == "azure_function"):
    inference_times, network_latency_times = faas_bench.run_bench(num_tasks, server_address, service_name, blob_connection_string=blob_connection_string, blob_container_name=blob_container_name)
  else:
    inference_times, network_latency_times = faas_bench.run_bench(num_tasks, server_address)
  for i in range(len(inference_times)):
    module_cw_logs.create_log_event(log_group_name, inference_time_log_stream_name, i+1, inference_times[i])
  for i in range(len(network_latency_times)):
    module_cw_logs.create_log_event(log_group_name, network_latency_time_log_stream_name, i+1, network_latency_times[i])
  
  #put_data_into_sheet.put_data(spreadsheet_id, worksheet_name, result, num_tasks)