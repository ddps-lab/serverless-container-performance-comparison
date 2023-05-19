import logging
import azure.functions as func
import json
import numpy as np
import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
model_folder = os.path.join(current_dir, "yolo_v5")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model(model_folder)
model_load_end_time = time.time()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    start_time = time.time()
    json_body = req.get_json()
    x = json_body['inputs']['x']
    result = model(np.array(x))
    end_time = time.time()
    response_data = json.dumps({
            'loading_time': model_load_end_time - model_load_start_time,
            'inference_time': end_time - start_time,
            'body': result.tolist()
        })
    return func.HttpResponse(
        status_code=200,
        headers={"Content-Type": "application/json"},
        body=response_data
    )