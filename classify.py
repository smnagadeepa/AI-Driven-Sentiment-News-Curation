import json

# File mapping for your categorized JSON files
file_mapping = {
    "business": "json/business_sentiment.json",
    "science": "json/science_sentiment.json",
    "entertainment": "json/entertainment_sentiment.json",
    "sports": "json/sports_sentiment.json",
    "technology": "json/technology_sentiment.json"
}

# Output sentiment JSON files
output_files = {
    "positive": "positive.json",
    "neutral": "neutral.json",
    "negative": "negative.json"
}

# Initialize empty lists for each sentiment
sentiment_data = {
    "positive": [],
    "neutral": [],
    "negative": []
}

# Iterate through each categorized file
for category, file_name in file_mapping.items():
    try:
        with open(file_name, 'r') as file:
            articles = json.load(file)  # Load the articles
            for article in articles:
                # Check the sentiment of the article
                sentiment = article.get("sentiment")
                if sentiment in sentiment_data:
                    sentiment_data[sentiment].append(article)  # Add to respective list
    except FileNotFoundError:
        print(f"File {file_name} not found. Skipping...")
    except json.JSONDecodeError:
        print(f"Error decoding {file_name}. Skipping...")

# Save articles to sentiment-specific JSON files
for sentiment, file_name in output_files.items():
    with open(file_name, 'w') as file:
        json.dump(sentiment_data[sentiment], file, indent=4)

print("Articles organized into sentiment-specific files.")