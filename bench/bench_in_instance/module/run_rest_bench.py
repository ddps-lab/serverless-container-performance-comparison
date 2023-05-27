from module import put_data_into_sheet
import importlib
rest_bench = ""

def main(model_name, num_tasks, server_address, spreadsheet_id, worksheet_name):
  global rest_bench
  rest_bench = importlib.import_module(f"{model_name}.rest_bench")
  result = rest_bench.run_bench(num_tasks, server_address)
  put_data_into_sheet.put_data(spreadsheet_id, worksheet_name, result, num_tasks)