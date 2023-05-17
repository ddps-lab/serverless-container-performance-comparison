from datetime import datetime
import variables
from module import put_data_into_sheet
import importlib
rest_bench = ""

def main(model_name, num_tasks, server_address, spreadsheet_id, worksheet_name, using_lambda=0, bucket_name=''):
  global rest_bench
  rest_bench = importlib.import_module(f"{model_name}.rest_bench")
  if (using_lambda == 1 and bucket_name != ''):
    result = rest_bench.run_bench(num_tasks, server_address, using_lambda=using_lambda, bucket_name=bucket_name)
  else:
    result = rest_bench.run_bench(num_tasks, server_address)
  put_data_into_sheet.put_data(spreadsheet_id, worksheet_name, result, num_tasks)

if (__name__ == "__main__"):
  now = datetime.now()
  worksheet_name = now.strftime("%y-%m-%d-%H:%M:%S")
  main(variables.model_name, variables.num_tasks, variables.rest_server_address, variables.rest_spreadsheet_id, worksheet_name)