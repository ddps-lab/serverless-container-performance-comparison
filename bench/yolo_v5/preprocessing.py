#image 전처리 library
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2

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
