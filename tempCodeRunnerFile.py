from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__, static_url_path='/static')

# Load the model and tokenizer
model = load_model('sentiment_model_lstm.h5')
tokenizer = Tokenizer(num_words=5000)

# Load your dataset to fit tokenizer and label encoder
df = pd.read_csv('preprocessed_news_sentiment.csv')  # Replace with your dataset path
tokenizer.fit_on_texts(df['text'])

# Label encoder to decode the predicted labels
label_encoder = LabelEncoder()
label_encoder.fit(df['label'])

# Function to predict sentiment
def predict_sentiment(text):
    # Tokenize and pad the input text
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=200)

    # Predict sentiment
    prediction = model.predict(padded_sequence)
    predicted_class = np.argmax(prediction, axis=1)[0]
    
    # Decode the label
    sentiment = label_encoder.inverse_transform([predicted_class])[0]
    return sentiment

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/iindex')
def iindex():
    return render_template('iindex.html')

@app.route('/live-news')
def live_news():
    # Retrieve the selected channel from the query parameter
    channel = request.args.get('channel', 'Default Channel')
    return render_template('live-news.html', channel=channel)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the text from the form input
    text = request.form['text']
    
    # Predict the sentiment
    sentiment = predict_sentiment(text)
    
    # Return the result
    return jsonify({'sentiment': sentiment})

if __name__ == '__main__':
    app.run(debug=True)
