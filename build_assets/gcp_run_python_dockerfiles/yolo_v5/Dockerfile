FROM python:3.10.11

WORKDIR /app

COPY ./models/yolo_v5 /app/yolo_v5

COPY ./build_assets/gcp_run_python_dockerfiles/requirements.txt /app

COPY ./build_assets/gcp_run_python_dockerfiles/yolo_v5/main.py /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8500

CMD ["python", "main.py"]

