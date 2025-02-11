import pandas as pd
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Step 1: Load the keyword datasets (handle CSV with or without headers)
try:
    # Try reading with a column header like 'keywords' or 'word'
    positive_keywords = pd.read_csv('datasets/positive.csv')['word'].tolist()
    negative_keywords = pd.read_csv('datasets/negative.csv')['word'].tolist()
except KeyError:
    # If headers are missing, read the first column directly
    positive_keywords = pd.read_csv('datasets/positive.csv', header=None)[0].tolist()
    negative_keywords = pd.read_csv('datasets/negative.csv', header=None)[0].tolist()

# Step 2: Load the entertainment.json file

try:
    with open('entertainment.json', 'r') as file:
        articles = json.load(file)
except FileNotFoundError:
    print("The file 'entertainment.json' does not exist. Please fetch and save the news data first.")
    exit()

# Step 3: Initialize the VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Step 4: Define a function to perform sentiment analysis using VADER
def determine_sentiment_vader(article_content):
    if article_content and isinstance(article_content, str):
        sentiment_score = analyzer.polarity_scores(article_content)
        # Based on the compound score, classify the sentiment
        if sentiment_score['compound'] >= 0.05:
            return "positive"
        elif sentiment_score['compound'] <= -0.05:
            return "negative"
        else:
            return "neutral"
    return "neutral"

# Step 5: Add sentiment field to each article
for article in articles:
    # Combine title and description for analysis (convert None to empty string)
    title = str(article.get('title', ''))
    description = str(article.get('description', ''))
    content = (title + " " + description).strip()
    
    # Use VADER for sentiment analysis
    sentiment = determine_sentiment_vader(content)
    article['sentiment'] = sentiment

# Step 6: Save the updated articles with sentiment analysis to a new JSON file
output_file = 'json/entertainment_sentiment.json'
with open(output_file, 'w') as file:
    json.dump(articles, file, indent=4)

print(f"News data with sentiment analysis using VADER has been saved to {output_file}.")