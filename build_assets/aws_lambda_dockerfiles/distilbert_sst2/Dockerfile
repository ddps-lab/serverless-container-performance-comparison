FROM aws_lambda_docker_base
COPY ./models/distilbert_sst2 ${LAMBDA_TASK_ROOT}/distilbert_sst2
COPY ./build_assets/aws_lambda_dockerfiles/distilbert_sst2/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]