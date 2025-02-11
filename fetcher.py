import requests
import json

API_KEY = "fcc0dbcd9f4646a89323102da51a035a"
query = "entertainment India"  # Adding "India" to the query to focus on Indian news
url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"

response = requests.get(url)

# Check if the API request was successful
if response.status_code == 200:
    data = response.json()
    articles = data['articles']

    # Print and save the articles
    for article in articles:
        print(article['title'], article['description'])

    with open('entertainment.json', 'w') as file:
        json.dump(articles, file, indent=4)

    print("Indian entertainment news has been saved to entertainment.json.")
else:
    print("Failed to fetch news:", response.status_code, response.reason)
