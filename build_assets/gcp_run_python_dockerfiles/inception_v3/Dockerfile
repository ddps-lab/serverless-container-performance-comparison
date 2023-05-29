FROM gcp_run_python_docker_base

WORKDIR /app

COPY ./models/inception_v3 /app/inception_v3

COPY ./build_assets/gcp_run_python_dockerfiles/inception_v3/main.py /app

EXPOSE 8500

CMD ["python", "main.py"]

