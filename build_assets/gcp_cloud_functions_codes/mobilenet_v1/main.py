import functions_framework
import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./mobilenet_v1')
model_load_end_time = time.time()

@functions_framework.http
def predict(request):
    if request.method == 'POST':
        start_time = time.time()
        json_body = request.get_json(silent=True)
        input_1 = json_body['inputs']['input_1']
        result = model.predict(np.array(input_1))
        end_time = time.time()
        response = {
            'statusCode': 200,
            'body': json.dumps({
                'loading_time': model_load_end_time - model_load_start_time,
                'inference_time': end_time - start_time,
                'body': result.tolist()
            })
        }
        return response
    else:
        return {
            'statusCode': 403,
            'body': "Please send POST request"
        }