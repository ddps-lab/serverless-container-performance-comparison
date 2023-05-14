FROM aws_lambda_docker_base
COPY ./models/bert_imdb ${LAMBDA_TASK_ROOT}/bert_imdb
COPY ./aws_lambda_dockerfiles/bert_imdb/app.py ${LAMBDA_TASK_ROOT}
CMD [ "app.lambda_handler" ]