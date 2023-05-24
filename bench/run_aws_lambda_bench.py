import aws_lambda_variables
import logs_variables
from module import module_cw_logs
from module import run_faas_bench
import time

def start_bench(model_names, num_tasks, aws_lambda_default_address, spreadsheet_id, bucket_name, log_group_name, log_stream_prefix):
  for i, model_name in enumerate(model_names):
    for k, num_task in enumerate(num_tasks):
      current_timestamp = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
      inference_time_log_stream_name = f"{current_timestamp}-{log_stream_prefix}-{model_name}-{num_task}-inference_time"
      network_latency_time_log_stream_name = f"{current_timestamp}-{log_stream_prefix}-{model_name}-{num_task}-inference_time"
      module_cw_logs.create_log_stream(log_group_name, inference_time_log_stream_name)
      module_cw_logs.create_log_stream(log_group_name, network_latency_time_log_stream_name)
      run_faas_bench.main(model_name,
                          num_task,
                          f"https://{model_name.replace('_','-')}.{aws_lambda_default_address}/",
                          spreadsheet_id,
                          f"{model_name}-{num_task}",
                          service_name="aws_lambda",
                          bucket_name=bucket_name,
                          log_group_name=log_group_name,
                          inference_time_log_stream_name=inference_time_log_stream_name,
                          network_latency_time_log_stream_name=network_latency_time_log_stream_name)
      time.sleep(5)

start_bench(aws_lambda_variables.model_names,
     aws_lambda_variables.num_tasks,
     aws_lambda_variables.aws_lambda_default_address,
     aws_lambda_variables.spreadsheet_id,
     aws_lambda_variables.bucket_name,
     logs_variables.log_group_name,
     logs_variables.log_stream_prefix)