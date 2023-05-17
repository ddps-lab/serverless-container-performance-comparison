import logging
import azure.functions as func
import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./mobilenet_v1')
model_load_end_time = time.time()

def main(req: func.HttpRequest) -> func.HttpResponse:
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