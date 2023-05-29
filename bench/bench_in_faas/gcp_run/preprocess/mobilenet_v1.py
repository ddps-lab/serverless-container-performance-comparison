#image 전처리 library
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow_serving.apis import predict_pb2
from tensorflow import make_tensor_proto
import numpy as np
from PIL import Image

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

def create_request_data():
    image_file_path = "../../../../dataset/imagenet/imagenet_1000_raw/n01843383_1.JPEG"
    data = predict_pb2.PredictRequest()
    data.model_spec.name = 'mobilenet_v1'
    data.model_spec.signature_name = 'serving_default'
    data.inputs['input_1'].CopyFrom(make_tensor_proto(run_preprocessing(image_file_path)))
    return data