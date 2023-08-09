#!/bin/bash
python3 grpc_main.py &
python3 push_metrics.py &
wait