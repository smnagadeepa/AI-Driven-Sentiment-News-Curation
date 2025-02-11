import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('punkt')

# Load the dataset
df = pd.read_csv("news_dataset.csv")

# Preprocess function
def preprocess_text(text):
    # Remove special characters
    text = re.sub(r'\W', ' ', text)
    # Lowercase the text
    text = text.lower()
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_tokens)

# Apply preprocessing
df['text'] = df['text'].apply(preprocess_text)

# Save the cleaned data to a new CSV file
df.to_csv("preprocessed_news_sentiment.csv", index=False)
print("Preprocessing completed and saved to 'preprocessed_news_sentiment.csv'")
