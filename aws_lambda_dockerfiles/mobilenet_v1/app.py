import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./mobilenet_v1')
model_load_end_time = time.time()

def lambda_handler(event,context):
    start_time = time.time()
    result = model.predict(event['body']['inputs']['input_1'])
    end_time = time.time()
    return {
        'statusCode': 200,
        'loading_time': model_load_end_time - model_load_start_time,
        'inference_time': end_time - start_time,
        'body': result
    }