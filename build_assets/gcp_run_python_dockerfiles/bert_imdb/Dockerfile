FROM python:3.10.11

WORKDIR /app

COPY ./models/bert_imdb /app/bert_imdb

COPY ./build_assets/gcp_run_python_dockerfiles/requirements.txt /app

COPY ./build_assets/gcp_run_python_dockerfiles/bert_imdb/main.py /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8500

CMD ["python", "main.py"]

