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
    bert_input_ids = tokenizer.texts_to_sequences([text])
    bert_input_ids = pad_sequences(bert_input_ids, maxlen=128, padding='post', truncating='post')
    bert_input_masks = [[1] * len(bert_input_ids[0])]

    return bert_input_ids, bert_input_masks

def create_request_data():
    text = "This is a sample sentence to test the BERT model."
    bert_input_ids, bert_input_masks = run_preprocessing(text)
    data = predict_pb2.PredictRequest()
    data.model_spec.name = 'distilbert_sst2'
    data.model_spec.signature_name = 'serving_default'
    data.inputs['bert_input_ids'].CopyFrom(make_tensor_proto(bert_input_ids, shape=[1,128]))
    data.inputs['bert_input_masks'].CopyFrom(make_tensor_proto(bert_input_masks, shape=[1,128]))
    return data