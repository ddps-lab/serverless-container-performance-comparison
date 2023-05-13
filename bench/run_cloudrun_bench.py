import cloudrun_variables
import run_grpc_bench
import run_grpc_each_session_bench
import run_rest_bench
import time

APIS = ["grpc", "each_grpc", "rest"]

def start_bench(model_names, num_tasks, cloud_run_address_default, grpc_use_https, spreadsheet_id):
  for i, model_name in enumerate(model_names):
    for j, api_name in enumerate(APIS):
      for k, num_task in enumerate(num_tasks):
        if (api_name == "grpc"):
          run_grpc_bench.main(model_name,
                              num_task,
                              f"{model_name.replace('_','-')}-grpc-{cloud_run_address_default}",
                              grpc_use_https,
                              spreadsheet_id,
                              f"{model_name}-{api_name}-{num_task}")
        elif (api_name == "each_grpc"):
            run_grpc_each_session_bench.main(model_name,
                                             num_task,
                                             f"{model_name.replace('_','-')}-grpc-{cloud_run_address_default}",
                                             grpc_use_https,
                                             spreadsheet_id,
                                             f"{model_name}-{api_name}-{num_task}")
        else:
            if (cloudrun_variables.grpc_use_https == 1):
              run_rest_bench.main(model_name,
                                  num_task,
                                  f"https://{model_name.replace('_','-')}-rest-{cloud_run_address_default}/",
                                  spreadsheet_id,
                                  f"{model_name}-{api_name}-{num_task}")
        time.sleep(5)

start_bench(cloudrun_variables.model_names,
     cloudrun_variables.num_tasks,
     cloudrun_variables.cloud_run_address_default,
     cloudrun_variables.grpc_use_https,
     cloudrun_variables.spreadsheet_id)