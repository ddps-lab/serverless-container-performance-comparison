#image 전처리 library
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow_serving.apis import predict_pb2
from tensorflow import make_tensor_proto
import numpy as np
import cv2
from google.protobuf.json_format import MessageToJson

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
    data = predict_pb2.PredictRequest()
    data.model_spec.name = 'yolo_v5'
    data.model_spec.signature_name = 'serving_default'
    data.inputs['x'].CopyFrom(make_tensor_proto(run_preprocessing(image_file_path)))
    json_data = MessageToJson(data)
    return json_data
