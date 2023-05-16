import json
import boto3
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
model_load_start_time = time.time()
import tensorflow as tf
model = tf.keras.models.load_model('./yolo_v5')
model_load_end_time = time.time()

def lambda_handler(event,context):
    start_time = time.time()
    json_body = json.loads(event['body'])
    s3_bucket_name = json_body['inputs']['s3_bucket_name']
    s3_object_name = json_body['inputs']['s3_object_name']
    s3 = boto3.resource('s3')
    s3.Bucket(s3_bucket_name).download_file(s3_object_name, "./preprocessed_data.npy")
    result = model(np.load("./preprocessed_data.npy"))
    np.save('predict_data', result)
    s3.Bucket(s3_bucket_name).upload_file("./predict_data.npy", "predict_data.npy")
    end_time = time.time()
    response = {
        'statusCode': 200,
        'body': json.dumps({
            'loading_time': model_load_end_time - model_load_start_time,
            'inference_time': end_time - start_time,
            'body': "S3 Uploaded"
        })
    }
    return response