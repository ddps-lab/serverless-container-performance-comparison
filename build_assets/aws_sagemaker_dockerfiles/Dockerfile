FROM 763104351884.dkr.ecr.ap-northeast-2.amazonaws.com/tensorflow-inference:2.11.1-cpu-py39-ubuntu20.04-sagemaker
COPY ./build_assets/aws_lambda_dockerfiles/requirements.txt .
RUN pip3 install --no-deps --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"