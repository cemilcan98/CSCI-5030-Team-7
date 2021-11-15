# -*- coding: utf-8 -*-
"""GEC_Baseline_Encoder_Decoder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GJ3WmjQO_Pvb9jn41ch9yoiZJHocQxZe

This notebook contains the following two steps for the task of Grammar Error Correction

3. Training Basic Model and debugging.

4. Tuning Basic Model.

## 3. Training the basic model and debugging
## 4. Tuning the basic model
"""

import io
import re
import datetime
import numpy as np
import pandas as pd
import random
from tqdm import tqdm
import tensorflow.keras
import tensorflow as tf
from sklearn.metrics import fbeta_score
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.layers import Embedding, LSTM, TimeDistributed, Dense, Bidirectional
from tensorflow.keras.initializers import HeNormal, GlorotNormal, GlorotUniform
from nltk.translate.bleu_score import sentence_bleu
import seaborn as sns
import matplotlib.pyplot as plt

"""Preprocess before tokenization :"""

data = pd.read_csv('preprocessed_15.csv')

pd.options.display.max_colwidth = 500
data[:50]

data[50:100]

"""Since preprocessing of data is already done before, all we do is add the tokens required to feed the
 data into our Encoder Decoder model with attention.
We implement the teacher forcing approach such that the the data looks like this: 
1. Encoder input: 
```
<start> Hello how are youz ? <end>
```
2. Decoder input: 
```
<start> Hello how are you ?
```
3. Decoder output: 
```
Hello how are you? <end>
```

This allows the decoder to always stay one step ahead during learning. 
"""


def preprocess(t, add_start_token, add_end_token):

    if add_start_token == True and add_end_token == False:
        t = '<start>'+' '+t
    if add_start_token == False and add_end_token == True:
        t = t+' '+'<end>'
    if add_start_token == True and add_end_token == True:
        t = '<start>'+' '+t+' '+'<end>'

    t = re.sub(' +', ' ', t)
    return t


encoder_input = [preprocess(
    line, add_start_token=True, add_end_token=True) for line in data['error']]
decoder_input = [preprocess(
    line, add_start_token=True, add_end_token=False) for line in data['correct']]
decoder_output = [preprocess(
    line, add_start_token=False, add_end_token=True) for line in data['correct']]

print(encoder_input[0])
print(decoder_input[0])
print(decoder_output[0])

"""Tokenization :"""

# ENCODER INPUT

tokenizer = Tokenizer(filters='', split=" ")
tokenizer.fit_on_texts(encoder_input)
word_index = tokenizer.word_index  # vocabulary

max_length = max([len(row.split(" ")) for row in encoder_input])
INPUT_ENCODER_LENGTH = max_length

enc_input_encoded = tokenizer.texts_to_sequences(encoder_input)
enc_input_padded = pad_sequences(
    enc_input_encoded, maxlen=INPUT_ENCODER_LENGTH, padding="post")

print(enc_input_padded.shape)

print(encoder_input[0])
print(enc_input_padded[0])

# DECODER INPUT
decoder_data = decoder_input.copy()
decoder_data.extend(decoder_output)

out_tokenizer = Tokenizer(filters='', split=" ")
out_tokenizer.fit_on_texts(decoder_data)
word_index = out_tokenizer.word_index  # vocabulary

max_length = max([len(row.split(" ")) for row in decoder_input])
INPUT_DECODER_LENGTH = max_length

dec_input_encoded = out_tokenizer.texts_to_sequences(decoder_input)
dec_input_padded = pad_sequences(
    dec_input_encoded, maxlen=INPUT_DECODER_LENGTH, padding="post", truncating="post")

print(dec_input_padded.shape)

print(decoder_input[0])
print(dec_input_padded[0])

dec_output_encoded = out_tokenizer.texts_to_sequences(decoder_output)
dec_output_padded = pad_sequences(
    dec_output_encoded, maxlen=INPUT_DECODER_LENGTH, padding="post", truncating="post")

print(dec_output_padded.shape)

print(decoder_output[1])
print(dec_output_padded[1])

"""#### FastText Embeddings"""

#!wget - -header = "Host: dl.fbaipublicfiles.com" - -header = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36" - -header = "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" - -header = "Accept-Language: en-US,en;q=0.9,kn;q=0.8" - -header = "Referer: https://fasttext.cc/" "https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip" - c - O 'wiki-news-300d-1M.vec.zip'

#!unzip wiki-news-300d-1M.vec.zip

# Reference: https://fasttext.cc/docs/en/english-vectors.html


def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = np.asarray(tokens[1:])  # map(float, tokens[1:])
    return data


embedding_index = load_vectors('wiki-news-300d-1M.vec')

# https://keras.io/examples/nlp/pretrained_word_embeddings/
word_index = tokenizer.word_index
num_tokens = len(word_index) + 2
embedding_dim = 300
hits = 0
misses = 0

embedding_matrix = np.zeros((num_tokens, embedding_dim))
for word, i in word_index.items():
    embedding_vector = embedding_index.get(word)

    if type(embedding_vector) == np.ndarray and embedding_vector.shape[0] == 300:
        embedding_matrix[i] = embedding_vector
        hits += 1

    else:
        misses += 1
print("Converted %d words (%d misses)" % (hits, misses))
np.save('GEC/test/in_embedding.npy', embedding_matrix)

word_index = out_tokenizer.word_index
num_tokens = len(word_index) + 2
embedding_dim = 300
hits = 0
misses = 0

embedding_matrix = np.zeros((num_tokens, embedding_dim))
for word, i in word_index.items():
    embedding_vector = embedding_index.get(word)

    if type(embedding_vector) == np.ndarray and embedding_vector.shape[0] == 300:
        embedding_matrix[i] = embedding_vector
        hits += 1

    else:
        misses += 1
print("Converted %d words (%d misses)" % (hits, misses))
np.save('GEC/test/out_embedding.npy', embedding_matrix)

"""#### VANILLA ENCODER DECODER"""

in_embedding_matrix = np.load(
    'GEC/test/in_embedding.npy')
out_embedding_matrix = np.load(
    'GEC/test/out_embedding.npy')
print(in_embedding_matrix.shape, out_embedding_matrix.shape)

# ENCODER


class Encoder(tf.keras.Model):
    def __init__(self, inp_vocab_size, embedding_size, lstm_size, input_length):
        super().__init__()
        self.vocab_size = inp_vocab_size
        self.embedding_size = embedding_size
        self.lstm_units = lstm_size
        self.input_length = input_length

    def build(self, input_sequence):
        # self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length,
        #                           #embeddings_initializer=keras.initializers.Constant(in_embedding_matrix), mask_zero=True,
        #                           weights = [in_embedding_matrix], mask_zero=True,
        #                           trainable = False, name="embedding_layer_encoder")
        self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length,
                                   mask_zero=True, name="embedding_layer_encoder")
        self.lstm = LSTM(self.lstm_units, return_state=True,
                         return_sequences=True, name="Encoder_LSTM")

    def call(self, input_sequence, states, training=True):
        # (batch_size, length of input array, embedding_size)
        input_embedding = self.embedding(input_sequence)
        self.lstm_output, self.state_h, self.state_c = self.lstm(
            input_embedding, initial_state=states)
        return self.lstm_output, self.state_h, self.state_c

    def initialize_states(self, batch_size):
        initializer = GlorotNormal()
        # tf.zeros((batch_size, self.lstm_units), dtype=tf.dtypes.float32, name="Encoder_LSTM_hidden_state")
        lstm_state_h = initializer(shape=(batch_size, self.lstm_units))
        # tf.zeros((batch_size, self.lstm_units), dtype=tf.dtypes.float32, name="Encoder_LSTM_cell_state")
        lstm_state_c = initializer(shape=(batch_size, self.lstm_units))
        return lstm_state_h, lstm_state_c

# DECODER


class Decoder(tf.keras.Model):
    def __init__(self, out_vocab_size, embedding_size, lstm_size, input_length):
        super().__init__()
        self.vocab_size = out_vocab_size
        self.embedding_size = embedding_size
        self.lstm_units = lstm_size
        self.input_length = input_length

    def build(self, input_sequence):
        # self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length,
        #                           #embeddings_initializer=keras.initializers.Constant(out_embedding_matrix),
        #                           weights = [out_embedding_matrix], mask_zero=True,
        #                           trainable = False, name="embedding_layer_decoder")
        self.embedding = Embedding(input_dim=self.vocab_size, output_dim=self.embedding_size, input_length=self.input_length,
                                   mask_zero=True, name="embedding_layer_decoder")
        self.lstm = LSTM(self.lstm_units, return_state=True,
                         return_sequences=True, name="Decoder_LSTM")

    def call(self, input_sequence, initial_states, training=True):

        input_embedding = self.embedding(input_sequence)
        self.lstm_output, self.state_h, self.state_c = self.lstm(
            input_embedding, initial_state=initial_states)
        return self.lstm_output, self.state_h, self.state_c


class Encoder_decoder(tf.keras.Model):

    def __init__(self, encoder_inputs_length, decoder_inputs_length, output_vocab_size):

        super().__init__()
        self.encoder = Encoder(INPUT_VOCAB_SIZE, embedding_size=256,
                               lstm_size=1200, input_length=INPUT_ENCODER_LENGTH)
        self.decoder = Decoder(
            OUTPUT_VOCAB_SIZE, embedding_size=256, lstm_size=1200, input_length=None)
        self.dense = Dense(output_vocab_size)  # , activation = 'softmax')

    def call(self, data):
        input, output = data[0], data[1]
        states = self.encoder.initialize_states(input.shape[0])
        encoder_output, encoder_final_state_h, encoder_final_state_c = self.encoder(
            input, states)
        decoder_output, decoder_state_h, decoder_state_c = self.decoder(
            output, [encoder_final_state_h, encoder_final_state_c])
        outputs = self.dense(decoder_output)

        return outputs


INPUT_VOCAB_SIZE = len(list(tokenizer.word_index)) + 1  # for zero padding +OOV
OUTPUT_VOCAB_SIZE = len(list(out_tokenizer.word_index)
                        ) + 1  # for zero padding + OOV
BATCH_SIZE = 16
print(INPUT_VOCAB_SIZE, INPUT_ENCODER_LENGTH,
      OUTPUT_VOCAB_SIZE, INPUT_DECODER_LENGTH, BATCH_SIZE)

"""#### Prepare data for feeding to model"""

# split into train and test from a tf.data object: https://stackoverflow.com/questions/48213766/split-a-dataset-created-by-tensorflow-dataset-api-in-to-train-and-test
NUMBER_OF_DATAPOINTS = 10000

tf.random.set_seed(32)

encoder_input_datatset = tf.data.Dataset.from_tensor_slices(enc_input_padded)
decoder_input_datatset = tf.data.Dataset.from_tensor_slices(dec_input_padded)
decoder_output_datatset = tf.data.Dataset.from_tensor_slices(dec_output_padded)

full_dataset = tf.data.Dataset.zip(((encoder_input_datatset.take(NUMBER_OF_DATAPOINTS), decoder_input_datatset.take(
    NUMBER_OF_DATAPOINTS)), decoder_output_datatset.take(NUMBER_OF_DATAPOINTS))).shuffle(1000)  # encoder_input_datatset.take(NUMBER_OF_DATAPOINTS).repeat(2)

test_dataset = full_dataset.take(50).batch(32)
train_dataset = full_dataset.skip(50).batch(32)

print(train_dataset, test_dataset)

"""#### Callback functions"""

# LEARNING RATE SCHEDULER: Decay learning rate after 15 epochs


def scheduler(epoch, lr):
    if epoch < 1:
        return lr
    else:
        return lr * tf.math.exp(-0.1)


lr_scheduler = tf.keras.callbacks.LearningRateScheduler(scheduler)

# EARLY STOPPING
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', patience=5, verbose=1)

# TENSORBOARD PLOTS
tensorboard_cb = tf.keras.callbacks.TensorBoard(log_dir='logs')

# SAVE MODEL WEIGHTS


class SaveModel(tf.keras.callbacks.Callback):

    def __init__(self):
        self.history = {'loss': [],  'val_loss': []}
        self.init = 0

    def on_epoch_end(self, epoch, logs={}):

        self.history['loss'].append(logs.get('loss'))
        if logs.get('val_loss', -1) != -1:
            self.history['val_loss'].append(logs.get('val_loss'))

        # if epochs % 10 == 0:
        # print('Saved weights for epoch {}!'.format(epoch))
        self.model.save_weights(
            'GEC/ENC_DEC_EMB/testweights_{}.h5'.format(epoch+self.init))

        df = pd.DataFrame(columns=['loss', 'val_loss'])
        for col in df.columns:
            df[col] = self.history[col]
        df.to_csv('history.csv')
        #!cp history.csv "/content/drive/MyDrive/Grammar/V4/ENC_DEC_EMB/history.csv"


save_model = SaveModel()

"""#### Loss function"""

# https://www.tensorflow.org/tutorials/text/image_captioning#model
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(
    from_logits=True, reduction='none'
)


def loss_function(real, pred):
    mask = tf.math.logical_not(tf.math.equal(real, 0))
    loss_ = loss_object(real, pred)

    mask = tf.cast(mask, dtype=loss_.dtype)
    loss_ *= mask

    return tf.reduce_mean(loss_)


"""#### Train with Vanilla Encoder Decoder"""

'''This code calculates the macro averaged fbeta score for each data point and outputs the mean of 32 scores'''


def f_beta_score(y_true, y_pred):
    y_pred_sparse = tf.convert_to_tensor(
        np.argmax(y_pred, axis=-1), dtype=tf.float32)
    fb_score = [fbeta_score(y_true[i], y_pred_sparse[i], average='macro', beta=0.5) for i in range(
        y_true.shape[0])]  # tf.py_function(fbeta_score, inp = [y, y_pred, 0.5], Tout=tf.float32)
    return sum(fb_score)/len(fb_score)


tf.config.run_functions_eagerly(True)

# Create an object of encoder_decoder Model class,
# Compile the model and fit the model
input = np.random.randint(0, 64, size=(BATCH_SIZE, INPUT_ENCODER_LENGTH))
output = np.random.randint(0, 64, size=(BATCH_SIZE, INPUT_DECODER_LENGTH))
# tf.keras.utils.to_categorical(output, OUTPUT_VOCAB_SIZE)
target = np.random.randint(0, 64, size=(BATCH_SIZE, INPUT_DECODER_LENGTH))

model = Encoder_decoder(encoder_inputs_length=INPUT_ENCODER_LENGTH,
                        decoder_inputs_length=INPUT_DECODER_LENGTH, output_vocab_size=OUTPUT_VOCAB_SIZE)
#model = encoder_decoder(enc_units = 1024, dec_units = 1024, scoring_func = 'dot', att_units = 1024)
model.compile(optimizer=tf.keras.optimizers.Adam(), loss=loss_function, metrics=[
              f_beta_score])  # tf.keras.metrics.categorical_crossentropy)
model.fit([input, output], target, steps_per_epoch=1)

model.summary()

"""WITH FASTTEXT EMBEDDINGS"""

# TEST1 1200 encoder decoder att units  #10000
'''
model.fit(train_dataset,
          validation_data=test_dataset,
          epochs=1,
          callbacks=[early_stopping, tensorboard_cb, save_model])
'''
# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir logs

"""WITHOUT FASTTEXT EMBEDDINGS"""

# TEST1 1200 encoder decoder att units  #1000
'''
model.fit(train_dataset,
          validation_data=test_dataset,
          epochs=1,
          callbacks=[early_stopping, tensorboard_cb, save_model])
'''
# Commented out IPython magic to ensure Python compatibility.
# %load_ext tensorboard
# %tensorboard --logdir logs

"""#### Inference for encoder-decoder"""

# model.load_weights('drive/MyDrive/GEC/ENC_DEC_EMB/weights_24_best.h5')
model.load_weights(
    'GEC\ENC_DEC_EMB\weights_0.h5')

# Input processor


def input_processor(input_sentence, pad_seq):

    # Preprocess to remove unwanted characters and convert to ASCII characters
    encoder_input = preprocess(
        input_sentence, add_start_token=True, add_end_token=True)

    # Convert to sequence
    tokenized_text = tokenizer.texts_to_sequences([encoder_input])
    if pad_seq == True:
        tokenized_text = pad_sequences(
            tokenized_text, maxlen=INPUT_ENCODER_LENGTH, padding="post")

    tokenized_text = tf.convert_to_tensor(tokenized_text, dtype=tf.float32)
    return tokenized_text


def remove_end_token(words):
    words_list = words.split(' ')[:-1]
    words = " ".join(words_list)
    return words
