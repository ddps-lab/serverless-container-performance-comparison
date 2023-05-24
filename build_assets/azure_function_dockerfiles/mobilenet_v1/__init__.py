import logging
import azure.functions as func
import json
import numpy as np
import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
model_folder = os.path.join(current_dir, "mobilenet_v1")
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
    input_1 = json_body['inputs']['input_1']
    result = model.predict(np.array(input_1))
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