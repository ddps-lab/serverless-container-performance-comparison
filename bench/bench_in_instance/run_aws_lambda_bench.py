import aws_lambda_variables
import logs_variables
from module import module_cw_logs
from module import run_faas_bench
import time

def start_bench(model_names, num_tasks, aws_lambda_default_address, spreadsheet_id, bucket_name, log_group_name):
  for i, model_name in enumerate(model_names):
    for k, num_task in enumerate(num_tasks):
      current_timestamp = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime())
      log_stream_name = f"{current_timestamp}-{model_name}-{num_task}tasks"
      module_cw_logs.create_log_stream(log_group_name, log_stream_name)
      run_faas_bench.main(model_name,
                          num_task,
                          f"https://{model_name.replace('_','-')}.{aws_lambda_default_address}/",
                          spreadsheet_id,
                          f"{model_name}-{num_task}",
                          service_name="aws_lambda",
                          bucket_name=bucket_name,
                          log_group_name=log_group_name,
                          log_stream_name=log_stream_name)
      time.sleep(5)

start_bench(aws_lambda_variables.model_names,
     aws_lambda_variables.num_tasks,
     aws_lambda_variables.aws_lambda_default_address,
     aws_lambda_variables.spreadsheet_id,
     aws_lambda_variables.bucket_name,
     logs_variables.log_group_name)