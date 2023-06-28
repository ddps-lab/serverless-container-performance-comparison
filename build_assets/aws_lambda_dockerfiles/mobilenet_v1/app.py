import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model('./mobilenet_v1')
model_load_end_time = time.time()

def lambda_handler(event,context):
    start_time = time.time()
    json_body = json.loads(event['body'])
    input_1 = json_body['inputs']['input_1']
    result = model.predict(np.array(input_1))
    end_time = time.time()
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'start_time': start_time,
            'loading_time': model_load_end_time - model_load_start_time,
            'inference_time': end_time - start_time,
            'body': result.tolist()
        })
    }
    return response