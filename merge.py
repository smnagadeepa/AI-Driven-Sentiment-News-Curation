import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk
import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Load JSON Files and Create a DataFrame
# Assuming the JSON files have a structure where 'content' contains the article text
with open('classified_json/positive.json', 'r') as f:
    positive_data = [{"text": article["content"], "label": "positive"} for article in json.load(f)]

with open('classified_json/negative.json', 'r') as f:
    negative_data = [{"text": article["content"], "label": "negative"} for article in json.load(f)]

with open('classified_json/neutral.json', 'r') as f:
    neutral_data = [{"text": article["content"], "label": "neutral"} for article in json.load(f)]

# Combine into a single dataset
data = pd.DataFrame(positive_data + negative_data + neutral_data)

# Step 2: Preprocessing Function
def preprocess_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'\d+', '', text)  # Remove numbers
    tokens = word_tokenize(text)  # Tokenize words
    tokens = [word for word in tokens if word not in stopwords.words('english')]  # Remove stopwords
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]  # Stem words
    return ' '.join(tokens)

# Step 3: Apply Preprocessing to the 'text' column
data['text'] = data['text'].apply(lambda x: preprocess_text(x) if isinstance(x, str) else preprocess_text(x['content']))

# Step 4: Feature Extraction - TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000)  # Set a limit on the number of features (adjust as needed)
X = vectorizer.fit_transform(data['text']).toarray()  # Transform text into feature vectors

# Step 5: Split the data into train and test sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, data['label'], test_size=0.2, random_state=42)

# Verify the split
print(f"Training data size: {X_train.shape[0]}")
print(f"Testing data size: {X_test.shape[0]}")

# Step 6: Train the Naive Bayes Classifier
model = MultinomialNB()
model.fit(X_train, y_train)

# Step 7: Make Predictions
y_pred = model.predict(X_test)

# Step 8: Evaluate the model
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print("Classification Report:")
print(classification_report(y_test, y_pred))