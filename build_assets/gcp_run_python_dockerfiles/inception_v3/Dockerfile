FROM python:3.10.11

WORKDIR /app

COPY ./models/inception_v3 /app/inception_v3

COPY ./build_assets/gcp_run_python_dockerfiles/requirements.txt /app

COPY ./build_assets/gcp_run_python_dockerfiles/inception_v3/main.py /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8500

CMD ["python", "main.py"]

