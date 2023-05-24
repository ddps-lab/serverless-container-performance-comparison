import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
from pathlib import Path
import json
import numpy as np
import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
model_folder = os.path.join(current_dir, "yolo_v5")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model(model_folder)
model_load_end_time = time.time()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    start_time = time.time()
    json_body = req.get_json()
    blob_container_name = json_body['inputs']['blob_container_name']
    blob_name = json_body['inputs']['blob_name']
    blob_service_client = BlobServiceClient.from_connection_string(os.environ.get("BlobStorageConnectionString"))
    container_client = blob_service_client.get_container_client(blob_container_name)
    with open("/tmp/preprocessed_data.npy", "wb") as file:
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob()
        blob_data.readinto(file)
    result = model(np.array(np.load("/tmp/preprocessed_data.npy")))
    np.save("/tmp/predict_data", result)
    with open("/tmp/predict_data.npy", "rb") as data:
        container_client.upload_blob(name="predict_data.npy", data=data, overwrite=True)
    end_time = time.time()
    response_data = json.dumps({
            'loading_time': model_load_end_time - model_load_start_time,
            'inference_time': end_time - start_time,
            'body': "Blob Uploaded"
        })
    return func.HttpResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=response_data
    )