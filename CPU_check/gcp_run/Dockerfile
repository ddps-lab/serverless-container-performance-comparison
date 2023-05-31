FROM python:3.10.11

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./main.py /app

EXPOSE 8501

CMD ["uvicorn", "main:main", "--port", "8501", "--host", "0.0.0.0"]

