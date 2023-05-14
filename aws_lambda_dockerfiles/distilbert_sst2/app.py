import json
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./bert_imdb')
model_load_end_time = time.time()

def lambda_handler(event, context):
    json_body = json.loads(event['body'])
    bert_input_ids = np.array(json_body['inputs']['bert_input_ids'])
    bert_input_masks = np.array(json_body['inputs']['bert_input_masks'])
    start_time = time.time()
    result = model.predict([bert_input_ids, bert_input_masks])
    end_time = time.time()
    print(result[0])
    return {
        'statusCode': 200,
        'loading_time': model_load_end_time - model_load_start_time,
        'body': end_time - start_time
    }