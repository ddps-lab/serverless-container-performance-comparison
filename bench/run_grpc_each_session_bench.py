import variables
from module import put_data_into_sheet
import importlib
grpc_bench = importlib.import_module(f"{variables.model_name}.grpc_each_session_bench")

result = grpc_bench.run_bench(variables.num_tasks, variables.grpc_server_address, variables.use_https)
put_data_into_sheet.put_data(variables.grpc_spreadsheet_id, result, variables.num_tasks)