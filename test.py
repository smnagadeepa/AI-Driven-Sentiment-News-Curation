import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load your dataset
df = pd.read_csv('preprocessed_news_sentiment.csv')  # Replace with your dataset path

# Encode labels (0: Negative, 1: Neutral, 2: Positive)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['label'])
for i in range(len(df)):
    if df.iloc[i]['label']=='negative':
        print(df.iloc[i])

# Tokenize the text
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(df['text'])
X = tokenizer.texts_to_sequences(df['text'])

# Pad the sequences to ensure uniform input size
X = pad_sequences(X, maxlen=200)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Load the trained model (if you have already saved the model)
model = load_model('sentiment_model_lstm.h5')

# Evaluate the model on the test data
y_pred = model.predict(X_test)
y_pred = np.argmax(y_pred, axis=1)  # Convert predictions to label indices

# Print accuracy and classification report
print("\nAccuracy:", accuracy_score(y_test, y_pred))  # Calculate accuracy
print("\nClassification Report:")
print(classification_report(y_test, y_pred))  # Print detailed classification report
