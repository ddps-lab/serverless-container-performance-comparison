FROM public.ecr.aws/lambda/python:3.11-preview
COPY ./aws_lambda_dockerfiles/yolo_v5/requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY ./models/yolo_v5 ${LAMBDA_TASK_ROOT}/yolo_v5
COPY ./aws_lambda_dockerfiles/yolo_v5/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]