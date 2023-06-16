#image 전처리 library
import os
import numpy as np
import cv2
import json
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

def create_request_data():
    image_file_path = "../../../../dataset/coco_2017/coco/images/val2017/000000000139.jpg"
    data = json.dumps({"inputs": {"x": run_preprocessing(image_file_path).tolist()}})
    return data
