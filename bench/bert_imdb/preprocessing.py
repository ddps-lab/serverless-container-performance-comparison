#image 전처리 library
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences

def run_preprocessing(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts([text])
    input_ids = tokenizer.texts_to_sequences([text])
    input_ids = pad_sequences(input_ids, maxlen=500, padding='post', truncating='post')
    input_masks = [[1] * len(input_ids[0])]
    segment_ids = [[0] * len(input_ids[0])]
    print(input_ids)
    print(input_masks)
    print(segment_ids)
    return input_ids, input_masks, segment_ids 

run_preprocessing("Test asdf asdf")