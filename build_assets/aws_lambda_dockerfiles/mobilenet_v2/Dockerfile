FROM aws_lambda_docker_base
COPY ./models/mobilenet_v2 ${LAMBDA_TASK_ROOT}/mobilenet_v2
COPY ./build_assets/aws_lambda_dockerfiles/mobilenet_v2/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]