import lambda_variables
import run_rest_bench
import time

def start_bench(model_names, num_tasks, lambda_address_default, spreadsheet_id, bucket_name=''):
  for i, model_name in enumerate(model_names):
    for k, num_task in enumerate(num_tasks):
      run_rest_bench.main(model_name,
                          num_task,
                          f"https://{model_name.replace('_','-')}.{lambda_address_default}/",
                          spreadsheet_id,
                          f"{model_name}-{num_task}",
                          using_lambda=1,
                          bucket_name=bucket_name)
      time.sleep(5)

start_bench(lambda_variables.model_names,
     lambda_variables.num_tasks,
     lambda_variables.lambda_address_default,
     lambda_variables.spreadsheet_id,
     lambda_variables.bucket_name)