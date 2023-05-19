#!/bin/bash
DOCKER_REGISTRY="asia-northeast3-docker.pkg.dev/cloudrun-inference/serverless-container-performance-comparison"
model_names=( "mobilenet_v1" "mobilenet_v2" "inception_v3" "yolo_v5" "bert_imdb" "distilbert_sst2" )
APIS=( "grpc" "rest" )

for model_name in "${model_names[@]}"
do
  for API in "${APIS[@]}"
  do
    sudo DOCKER_BUILDKIT=1 docker build -t $DOCKER_REGISTRY/gcp-run-$model_name-$API:latest -f ./gcp_run_dockerfiles/$model_name/Dockerfile.$API .
  done
done

for model_name in "${model_names[@]}"
do
  for API in "${APIS[@]}"
  do
    sudo docker push $DOCKER_REGISTRY/gcp-run-$model_name-$API:latest
  done
done