FROM gcp_run_python_docker_base

WORKDIR /app

COPY ./models/bert_imdb /app/bert_imdb

COPY ./build_assets/gcp_run_python_dockerfiles/bert_imdb/main.py /app

EXPOSE 8500

CMD ["python", "main.py"]

