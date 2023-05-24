import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
from tensorflow.keras.models import load_model
model = load_model('./bert_imdb')
model_load_end_time = time.time()

def lambda_handler(event, context):
    start_time = time.time()
    json_body = json.loads(event['body'])
    input_ids = np.array(json_body['inputs']['input_ids'])
    input_masks = np.array(json_body['inputs']['input_masks'])
    segment_ids = np.array(json_body['inputs']['segment_ids'])
    result = model.predict([input_masks, input_ids, segment_ids])
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