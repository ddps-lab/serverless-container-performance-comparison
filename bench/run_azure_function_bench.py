import azure_function_variables
from module import run_faas_bench
import time

def start_bench(model_names, num_tasks, azure_function_default_address, spreadsheet_id):
  for i, model_name in enumerate(model_names):
    for k, num_task in enumerate(num_tasks):
      run_faas_bench.main(model_name,
                          num_task,
                          f"https://{model_name.replace('_','-')}{azure_function_default_address}/",
                          spreadsheet_id,
                          f"{model_name}-{num_task}",
                          service_name="azure_function",)
      time.sleep(5)

start_bench(azure_function_variables.model_names,
     azure_function_variables.num_tasks,
     azure_function_variables.azure_function_default_address,
     azure_function_variables.spreadsheet_id,
     )