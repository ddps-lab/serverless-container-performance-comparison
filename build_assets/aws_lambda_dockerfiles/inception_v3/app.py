import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./inception_v3')
model_load_end_time = time.time()

def lambda_handler(event,context):
    start_time = time.time()
    json_body = json.loads(event['body'])
    input_3 = json_body['inputs']['input_3']
    result = model.predict(np.array(input_3))
    end_time = time.time()
    print(result[0])
    return {
        'statusCode': 200,
        'loading_time': model_load_end_time - model_load_start_time,
        'body': end_time - start_time
    }