import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

# Load your dataset
df = pd.read_csv('preprocessed_news_sentiment.csv')

# Encode labels (0: Negative, 1: Neutral, 2: Positive)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['label'])

# Tokenize the text
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df['text'])
X = tokenizer.texts_to_sequences(df['text'])

# Pad the sequences to ensure uniform input size
X = pad_sequences(X, maxlen=200)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the LSTM model
model = Sequential()


# Embedding layer to convert words to dense vectors
model.add(Embedding(input_dim=5000, output_dim=128, input_length=200))

# LSTM layer to capture sequential patterns
model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))

# Dense layer for classification output
model.add(Dense(3, activation='softmax'))

# Compile the model
model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Now evaluate the model on the test data
score, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy}")

# Save the trained model
model.save('sentiment_model_lstm.h5')