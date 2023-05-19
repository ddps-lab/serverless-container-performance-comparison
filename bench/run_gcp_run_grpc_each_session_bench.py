import gcp_run_variables
from module import run_grpc_each_session_bench
import time

def start_bench(model_names, num_tasks, gcp_run_default_address, grpc_use_https, spreadsheet_id):
  for i, model_name in enumerate(model_names):
    for k, num_task in enumerate(num_tasks):
      run_grpc_each_session_bench.main(model_name,
                                        num_task,
                                        f"{model_name.replace('_','-')}-grpc-{gcp_run_default_address}",
                                        grpc_use_https,
                                        spreadsheet_id,
                                        f"{model_name}-grpc-each-session-{num_task}")
      time.sleep(5)

start_bench(gcp_run_variables.model_names,
     gcp_run_variables.num_tasks,
     gcp_run_variables.gcp_run_default_address,
     gcp_run_variables.grpc_use_https,
     gcp_run_variables.spreadsheet_id)