#!/bin/bash
source ./variables.sh

# warm bench request lambda instances
go run run_bench.go --model_name "unknown" --task_num 100 --log_group_name "unknown" --server_address $server_address --aws_sagemaker_endpoint_prefix "unknown" --s3_bucket_name $s3_bucket_name --s3_preprocessed_data_key_path $s3_preprocessed_data_key_path
sleep 5
go run run_bench.go --model_name "unknown" --task_num 100 --log_group_name "unknown" --server_address $server_address --aws_sagemaker_endpoint_prefix "unknown" --s3_bucket_name $s3_bucket_name --s3_preprocessed_data_key_path $s3_preprocessed_data_key_path
sleep 5
for model_name in "${model_names[@]}"
do
  for task_num in "${task_nums[@]}"
  do
    go run run_bench.go --model_name $model_name --task_num $task_num --log_group_name $log_group_name --server_address $server_address --aws_sagemaker_endpoint_prefix $aws_sagemaker_endpoint_prefix --s3_bucket_name $s3_bucket_name --s3_preprocessed_data_key_path $s3_preprocessed_data_key_path
    sleep 5
  done
done