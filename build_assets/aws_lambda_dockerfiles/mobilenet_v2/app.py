import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./mobilenet_v2')
model_load_end_time = time.time()

def lambda_handler(event,context):
    start_time = time.time()
    json_body = json.loads(event['body'])
    input_2 = json_body['inputs']['input_2']
    result = model.predict(np.array(input_2))
    end_time = time.time()
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'loading_time': model_load_end_time - model_load_start_time,
            'inference_time': end_time - start_time,
            'body': result
        })
    }
    return response