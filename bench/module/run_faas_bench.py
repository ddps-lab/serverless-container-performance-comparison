from module import put_data_into_sheet
import importlib
faas_bench = ""

def main(model_name, num_tasks, server_address, spreadsheet_id, worksheet_name, service_name, bucket_name=''):
  global faas_bench
  if (model_name == "yolo_v5" and service_name == "aws_lambda"):
    faas_bench = importlib.import_module(f"{model_name}.lambda_bench")
    result = faas_bench.run_bench(num_tasks, server_address, service_name, bucket_name)
  else:
    faas_bench = importlib.import_module(f"{model_name}.faas_bench")
    result = faas_bench.run_bench(num_tasks, server_address)
  put_data_into_sheet.put_data(spreadsheet_id, worksheet_name, result, num_tasks)