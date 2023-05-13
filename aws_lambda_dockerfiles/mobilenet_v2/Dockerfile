FROM public.ecr.aws/lambda/python:3.11-preview
COPY ./aws_lambda_dockerfiles/requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY ./models/mobilenet_v2 ${LAMBDA_TASK_ROOT}/mobilenet_v2
COPY ./aws_lambda_dockerfiles/mobilenet_v2/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]