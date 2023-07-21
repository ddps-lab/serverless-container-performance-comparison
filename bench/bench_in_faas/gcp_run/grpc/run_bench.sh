#!/bin/bash
source ./variables.sh

# warm bench request lambda instances
go run run_bench.go --model_name "unknown" --task_num 100 --log_group_name "unknown" --server_address $server_address --gcp_run_prefix "unknown" --gcp_run_default_address "unknown" --use_https $use_https
sleep 5
go run run_bench.go --model_name "unknown" --task_num 100 --log_group_name "unknown" --server_address $server_address --gcp_run_prefix "unknown" --gcp_run_default_address "unknown" --use_https $use_https
sleep 5
for model_name in "${model_names[@]}"
do
  for task_num in "${task_nums[@]}"
  do
    go run run_bench.go --model_name $model_name --task_num $task_num --log_group_name $log_group_name --server_address $server_address --gcp_run_prefix $gcp_run_prefix --gcp_run_default_address $gcp_run_default_address --use_https $use_https
    sleep 30
  done
done