FROM aws_lambda_docker_base
COPY ./models/yolo_v5 ${LAMBDA_TASK_ROOT}/yolo_v5
COPY ./aws_lambda_dockerfiles/yolo_v5/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]