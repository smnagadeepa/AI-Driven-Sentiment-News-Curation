import tensorflow as tf
print(tf.__version__)
from tensorflow.keras.preprocessing.text import Tokenizer
print("Tokenizer imported successfully!")
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Example text data (replace this with your actual CSV loading code)
data = ['This is a positive example', 'This is a negative example', 'Neutral sentiment here']

# Initialize the Tokenizer
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(data)

# Convert texts to sequences
sequences = tokenizer.texts_to_sequences(data)
print("Sequences:", sequences)

# Pad sequences to make them uniform in length
padded_sequences = pad_sequences(sequences, maxlen=10)
print("Padded Sequences:", padded_sequences)
