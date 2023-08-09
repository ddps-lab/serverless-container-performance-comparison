import os
import requests
import subprocess
import multiprocessing
import time
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
from urllib.parse import quote

def get_process_cpu_utilization(num_cores):
    command = """top -b -n1 -c | awk 'NR>7 {printf $9" "; for (i=12; i<=NF; i++) printf $i " "; print ""}'"""
    ps_output = subprocess.check_output(command, shell=True).decode('utf-8')

    lines = ps_output.strip().split('\n')

    all_cpu_usage = 0
    cpu_values = []
    command_values = []
    for line in lines:
        cpu, command = line.split(None, 1)
        command = quote(command.strip())
        cpu_values.append(float(cpu))
        all_cpu_usage += float(cpu)
        command_values.append(command.strip())
    all_cpu_usage = all_cpu_usage / num_cores
    
    return all_cpu_usage, cpu_values, command_values


if __name__ == "__main__":
    pushgateway_address = os.environ['PUSHGATEWAY_ADDRESS']
    model_name = os.environ['MODEL_NAME']
    ram_size = os.environ['RAM_SIZE']
    metadata_url = "http://metadata.google.internal/computeMetadata/v1/instance/id"
    metadata_headers = {'Metadata-Flavor': 'Google'}
    container_instance_id = (requests.get(metadata_url, headers=metadata_headers)).text
    num_cores = multiprocessing.cpu_count()
    registry1 = CollectorRegistry()
    registry2 = CollectorRegistry()
    cpu_usage_gauge = Gauge('cpu_usage', 'CPU usage from ps command', registry=registry1)
    process_cpu_usage_gauge = Gauge('process_cpu_usage', 'Process CPU usage from ps command', registry=registry2)
    while True:
        all_cpu_usage, process_cpu_usages, process_commands = get_process_cpu_utilization(num_cores)
        if (all_cpu_usage != None):
            cpu_usage_gauge.set(all_cpu_usage)
            try:
                push_to_gateway(pushgateway_address, job='cloud_run', registry=registry1, grouping_key={'container_instance_id': container_instance_id[-20:], 'model_name': model_name, 'ram_size': ram_size, 'num_cores': num_cores})
            except Exception as e:
                print("connection refused")
                time.sleep(1)
            for index, (process_cpu_usage, process_command) in enumerate(zip(process_cpu_usages, process_commands)):
                process_cpu_usage_gauge.set(process_cpu_usage)
                try:
                    push_to_gateway(pushgateway_address, job='cloud_run', registry=registry2, grouping_key={'container_instance_id': container_instance_id[-20:], 'process_command': process_command, 'model_name': model_name, 'ram_size': ram_size, 'num_cores': num_cores})
                except Exception as e:
                    print("connection refused")
                    time.sleep(1)
        time.sleep(0.1)