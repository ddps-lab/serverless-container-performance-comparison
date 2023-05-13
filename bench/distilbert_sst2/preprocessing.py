#image 전처리 library
import tensorflow as tf

def run_preprocessing(text):
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts([text])
    bert_input_ids = tokenizer.texts_to_sequences([text])
    bert_input_mask = [[1] * len(bert_input_ids[0])]

    return bert_input_ids, bert_input_mask