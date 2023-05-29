FROM gcp_run_python_docker_base

WORKDIR /app

COPY ./models/mobilenet_v1 /app/mobilenet_v1

COPY ./build_assets/gcp_run_python_dockerfiles/mobilenet_v1/main.py /app

EXPOSE 8500

CMD ["python", "main.py"]

