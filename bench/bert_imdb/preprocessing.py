#image 전처리 library
import tensorflow as tf

def run_preprocessing(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts([text])
    input_ids = tokenizer.texts_to_sequences([text])
    input_mask = [[1] * len(input_ids[0])]
    segment_ids = [[0] * len(input_ids[0])]

    return input_ids, input_mask, segment_ids 