FROM aws_lambda_docker_base
COPY ./models/inception_v3 ${LAMBDA_TASK_ROOT}/inception_v3
COPY ./build_assets/aws_lambda_dockerfiles/inception_v3/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]