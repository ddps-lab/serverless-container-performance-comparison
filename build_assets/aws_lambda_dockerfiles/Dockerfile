FROM public.ecr.aws/lambda/python:3.10
COPY ./build_assets/aws_lambda_dockerfiles/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"