import functions_framework
import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model('./inception_v3')
model_load_end_time = time.time()

@functions_framework.http
def predict(request):
    if request.method == 'POST':
        start_time = time.time()
        json_body = request.get_json(silent=True)
        input_3 = json_body['inputs']['input_3']
        result = model.predict(np.array(input_3))
        end_time = time.time()
        response = json.dumps({
                'loading_time': model_load_end_time - model_load_start_time,
                'inference_time': end_time - start_time,
                'body': result.tolist()
        })
        return response, 200, {'Content-Type': 'application/json'}
    else:
        return json.dumps({
            'body': "Please send POST request"
        }), 403, {'Content-Type': 'application/json'}