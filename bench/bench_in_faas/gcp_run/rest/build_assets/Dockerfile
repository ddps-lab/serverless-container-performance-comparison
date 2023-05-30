FROM python:3.10.11

WORKDIR /app

COPY ./bench/bench_in_faas/gcp_run/rest/build_assets/requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./bench/bench_in_faas/gcp_run/rest/build_assets/main.py /app

EXPOSE 8501

CMD ["uvicorn", "main:app", "--port", "8501", "--host", "0.0.0.0"]
