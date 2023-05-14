import functions_framework
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./yolo_v5')
model_load_end_time = time.time()

@functions_framework.http
def predict(request):
    if request.method == 'POST':
        start_time = time.time()
        json_body = request.get_json(silent=True)
        x = json_body['inputs']['x']
        result = model.predict(np.array(x))
        end_time = time.time()
        print(result[0])
        return {
            'statusCode': 200,
            'loading_time': model_load_end_time - model_load_start_time,
            'body': end_time - start_time
        }
    else:
        return {
            'statusCode': 403,
            'body': "Please send POST request"
        }