#!/bin/bash
nohup python3 push_metrics.py &
python3 grpc_main.py