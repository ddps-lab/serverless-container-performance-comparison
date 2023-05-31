import os
import multiprocessing
import subprocess
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def main():
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    mem_gib = mem_bytes/(1024.**3)
    num_cores = multiprocessing.cpu_count()
    cpu_info = subprocess.check_output ('cat /proc/cpuinfo', shell=True)
    mem_info = subprocess.check_output('cat /proc/meminfo', shell=True)

    response = {
        "mem_bytes": mem_bytes,
        "mem_gib": mem_gib,
        "num_cores": num_cores,
        "cpu_info": cpu_info,
        "mem_info": mem_info
    }
    return response
