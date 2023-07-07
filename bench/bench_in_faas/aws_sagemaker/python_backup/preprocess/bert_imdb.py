#image 전처리 library
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from keras.utils import pad_sequences
import json

def run_preprocessing(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts([text])
    input_ids = tokenizer.texts_to_sequences([text])
    input_ids = pad_sequences(input_ids, maxlen=500, padding='post', truncating='post')
    input_masks = [[1] * len(input_ids[0])]
    segment_ids = [[0] * len(input_ids[0])]
    return input_ids, input_masks, segment_ids 

def create_request_data(bucket_name=""):
    text = "This is a sample sentence to test the BERT model."
    input_ids, input_masks, segment_ids = run_preprocessing(text)
    data = json.dumps({"inputs": { "segment_ids": segment_ids, "input_masks": input_masks, "input_ids": input_ids.tolist()}})
    return data, 0