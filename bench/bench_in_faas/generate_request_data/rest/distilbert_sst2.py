#image 전처리 library
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from keras.utils import pad_sequences
import json

def run_preprocessing(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts([text])
    bert_input_ids = tokenizer.texts_to_sequences([text])
    bert_input_ids = pad_sequences(bert_input_ids, maxlen=128, padding='post', truncating='post')
    bert_input_masks = [[1] * len(bert_input_ids[0])]

    return bert_input_ids, bert_input_masks

def create_request_data():
    text = "This is a sample sentence to test the BERT model."
    bert_input_ids, bert_input_masks = run_preprocessing(text)
    data = {"inputs": { "bert_input_masks": bert_input_masks, "bert_input_ids": bert_input_ids.tolist()}}
    with open("distilbert_sst2.json", "w") as file:
        json.dump(data, file)

if __name__ == '__main__':
    create_request_data()
