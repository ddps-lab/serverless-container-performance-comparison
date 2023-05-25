#image 전처리 library
import os
import numpy as np
from PIL import Image
import json

def get_file_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

# 이미지 로드 및 전처리 (for mobilenet)
def run_preprocessing(image_file_path):
    img = Image.open(get_file_path(image_file_path))
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = img_array.astype('float32') / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def create_request_data(bucket_name=''):
    image_file_path = "../../../../dataset/imagenet/imagenet_1000_raw/n01843383_1.JPEG"
    data = json.dumps({"inputs": { "input_2": run_preprocessing(image_file_path).tolist()}})
    return data, 0
