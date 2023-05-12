from datetime import datetime
import numpy as np
# google sheet api 관련 library
from module import module_gspread

def put_data(spreadsheet_id, array, num_tasks):
    now = datetime.now()
    formatted_date = now.strftime("%y-%m-%d-%H:%M:%S")
    spread_doc = module_gspread.open_sheet(spreadsheet_id)
    open_worksheet = spread_doc.add_worksheet(
        title=formatted_date, rows=10+num_tasks, cols=10)
    open_worksheet.update(
        'A1', "elapsed_inference_time (network latency included)")
    open_worksheet.merge_cells("A1:C1")
    open_worksheet.update('A2', "Minimum time")
    open_worksheet.update(
        'A3', f"=MIN(A6:A{6+num_tasks-1})", value_input_option='USER_ENTERED')
    open_worksheet.update('B2', "Maximum time")
    open_worksheet.update(
        'B3', f"=MAX(A6:A{6+num_tasks-1})", value_input_option='USER_ENTERED')
    open_worksheet.update('C2', "Average time")
    open_worksheet.update(
        'C3', f"=AVERAGE(A6:A{6+num_tasks-1})", value_input_option='USER_ENTERED')
    open_worksheet.update('A5', "times")

    cell_list = open_worksheet.range(f'A6:A{6+num_tasks-1}')
    for i, cell in enumerate(cell_list):
        cell.value = array[i]
    open_worksheet.update_cells(cell_list)
