FROM public.ecr.aws/lambda/python:3.11-preview
COPY ./aws_lambda_dockerfiles/inception_v3/requirements.txt .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY ./models/inception_v3 ${LAMBDA_TASK_ROOT}/inception_v3
COPY ./aws_lambda_dockerfiles/inception_v3/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]