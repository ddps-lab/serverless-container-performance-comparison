#image 전처리 library
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow_serving.apis import predict_pb2
from tensorflow import make_tensor_proto
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences

def run_preprocessing(text):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts([text])
    input_ids = tokenizer.texts_to_sequences([text])
    input_ids = pad_sequences(input_ids, maxlen=500, padding='post', truncating='post')
    input_masks = [[1] * len(input_ids[0])]
    segment_ids = [[0] * len(input_ids[0])]
    return input_ids, input_masks, segment_ids 

def create_request_data():
    text = "This is a sample sentence to test the BERT model."
    input_ids, input_masks, segment_ids = run_preprocessing(text)
    data = predict_pb2.PredictRequest()
    data.model_spec.name = 'bert_imdb'
    data.model_spec.signature_name = 'serving_default'
    data.inputs['input_ids'].CopyFrom(make_tensor_proto(input_ids, shape=[1, len(input_ids[0])]))
    data.inputs['input_masks'].CopyFrom(make_tensor_proto(input_masks, shape=[1, len(input_masks[0])]))
    data.inputs['segment_ids'].CopyFrom(make_tensor_proto(segment_ids, shape=[1, len(segment_ids[0])]))
    return data