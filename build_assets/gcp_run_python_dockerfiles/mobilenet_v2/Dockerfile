FROM gcp_run_python_docker_base

WORKDIR /app

COPY ./models/mobilenet_v2 /app/mobilenet_v2

COPY ./build_assets/gcp_run_python_dockerfiles/mobilenet_v2/main.py /app

EXPOSE 8500

CMD ["python", "main.py"]

