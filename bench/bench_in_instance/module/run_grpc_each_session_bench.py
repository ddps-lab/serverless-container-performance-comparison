from module import put_data_into_sheet
import importlib
grpc_bench = ""

def main(model_name, num_tasks, server_address, use_https, spreadsheet_id, worksheet_name):
  global grpc_bench
  grpc_bench = importlib.import_module(f"{model_name}.grpc_each_session_bench")
  result = grpc_bench.run_bench(num_tasks, server_address, use_https)
  put_data_into_sheet.put_data(spreadsheet_id, worksheet_name, result, num_tasks)