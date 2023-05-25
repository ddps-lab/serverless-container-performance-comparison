#image 전처리 library
import os
import numpy as np
import cv2
import json
import boto3
import time

def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# 이미지 로드 및 전처리 (for yolo)
def run_preprocessing(image_file_path):
    img = cv2.imread(get_file_path(image_file_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def create_request_data(bucket_name=''):
    image_file_path = "../../../../dataset/coco_2017/coco/images/val2017/000000000139.jpg"
    
    np.save('preprocessed_data', run_preprocessing(image_file_path))
    s3 = boto3.resource('s3')
    upload_start_time = time.time()
    s3.Bucket(bucket_name).upload_file('./preprocessed_data.npy', "preprocessed_data.npy")
    upload_time = time.time() - upload_start_time
    data = json.dumps({"inputs": {"s3_bucket_name": bucket_name, "s3_object_name": "preprocessed_data.npy"}})
    return data, upload_time
