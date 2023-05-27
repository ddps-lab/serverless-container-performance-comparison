import gcp_functions_variables
from module import run_faas_bench
import time

def start_bench(model_names, num_tasks, gcp_functions_default_address, spreadsheet_id, bucket_name=""):
  for i, model_name in enumerate(model_names):
    for k, num_task in enumerate(num_tasks):
      run_faas_bench.main(model_name,
                          num_task,
                          f"https://{gcp_functions_default_address}.cloudfunctions.net/function-{model_name.replace('_','-')}",
                          spreadsheet_id,
                          f"{model_name}-{num_task}",
                          service_name="gcp_functions")
      time.sleep(5)

start_bench(gcp_functions_variables.model_names,
     gcp_functions_variables.num_tasks,
     gcp_functions_variables.gcp_functions_default_address,
     gcp_functions_variables.spreadsheet_id,)