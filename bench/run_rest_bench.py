import variables
from module import put_data_into_sheet
import importlib
rest_bench = importlib.import_module(f"{variables.model_name}.rest_bench")

result = rest_bench.run_bench(variables.num_tasks, variables.rest_server_address)

put_data_into_sheet.put_data(variables.rest_spreadsheet_id, result, variables.num_tasks)