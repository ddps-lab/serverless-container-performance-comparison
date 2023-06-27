#image 전처리 library
import os
import numpy as np
from PIL import Image
import json
import boto3
import time

def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# 이미지 로드 및 전처리 (for inception)
def run_preprocessing(image_file_path):
    img = Image.open(get_file_path(image_file_path))
    img = img.resize((299, 299))
    img_array = np.array(img)
    img_array = (img_array - np.mean(img_array)) / np.std(img_array) 
    img_array = img_array.astype(np.float32)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def create_request_data(bucket_name=""):
    image_file_path = "../../../../dataset/imagenet/imagenet_1000_raw/n01843383_1.JPEG"
    
    np.save('preprocessed_data', run_preprocessing(image_file_path))
    s3 = boto3.resource('s3')
    upload_start_time = time.time()
    s3.Bucket(bucket_name).upload_file('./preprocessed_data.npy', "preprocessed_data.npy")
    upload_time = time.time() - upload_start_time
    data = json.dumps({"inputs": {"s3_bucket_name": bucket_name, "s3_object_name": "preprocessed_data.npy"}})
    return data, upload_time
