const API_KEY = "05c40b9ae2b948f2a0204c0316913520";
const url = "https://newsapi.org/v2/everything?q=";

async function fetchNews(query) {
    const requestUrl = await fetch(`${url}${query}&apiKey=${API_KEY}&language=en&sortBy=publishedAt`);
    const data = await requestUrl.json();
    bindData(data.articles);
}
window.addEventListener("load", () => fetchNews("India"));

function bindData(articles) {
    const cardsContainer = document.getElementById("cards-container");
    const newsCardTemplate = document.getElementById("template-news-card");

    cardsContainer.innerHTML = "";

    const seenTitles = new Set();

    const filteredArticles = articles.filter((article) => {
        const hasValidImage = article.urlToImage && article.urlToImage.trim() !== "";
        const hasValidTitle = article.title && article.title.trim() !== "";
        const hasValidDescription = article.description && article.description.trim() !== "";
        
        if (!hasValidImage || !hasValidTitle || !hasValidDescription) {
            return false;
        }

        const normalizedTitle = article.title.trim().toLowerCase();

        if (seenTitles.has(normalizedTitle)) {
            return false;
        }

        seenTitles.add(normalizedTitle);
        return true;
    });

    if (filteredArticles.length === 0) {
        cardsContainer.innerHTML = "<p>No relevant news articles found.</p>";
        return;
    }

    filteredArticles.forEach((article) => {
        const cardClone = newsCardTemplate.content.cloneNode(true);
        fetch('/predict', {
            method: 'POST',
            body: new URLSearchParams('text=' + article.description),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            
            //document.getElementById('sentiment').textContent = data.sentiment;
            fillDataInCard(cardClone, article,data.sentiment);
            cardsContainer.appendChild(cardClone);
        })
        .catch(error => console.error('Error:', error));
        
        
    });
}

function fillDataInCard(cardClone, article,senti) {
    const newsImg = cardClone.querySelector("#news-img");
    const newsTitle = cardClone.querySelector("#news-title");
    const newsSource = cardClone.querySelector("#news-source");
    const newsDesc = cardClone.querySelector("#news-desc");
    const sentimentIcon = cardClone.querySelector('#sentiment-icon');

    newsImg.src = article.urlToImage || "file:///C:/Users/Admin/Desktop/Nagadeepa%20Project/images/placeholder.png";
    newsTitle.innerHTML = article.title || "No Title Available";
    const sentiIcon = getSentimentIcon(senti); 
    sentimentIcon.innerHTML=(sentiIcon);
    newsDesc.innerHTML = article.description || "No description available.";

    const date = new Date(article.publishedAt).toLocaleString("en-US", {
        timeZone: "Asia/Jakarta",
    });
    newsSource.innerHTML = `${article.source.name || "Unknown Source"} · ${date}`;

    cardClone.firstElementChild.addEventListener("click", () => {
        window.open(article.url, "_blank");
    });
}

let curSelectedNav = null;

function onNavItemClick(id) {
    fetchNews(id); // Pass the country code for India
}

function redirectToYouTube() {
    var selectedChannel = document.getElementById("channel-select").value;
    if (selectedChannel) {
        window.location.href = selectedChannel; // Redirect to the URL
    }
}


function searchNews() {
    const query = document.querySelector('.news-input').value.trim();
    fetchNews(query);
}


function getSentimentIcon(sentiment) {
    //alert(sentiment);
    switch (sentiment) {
       
        case 'positive':
            return ' <i class="fas fa-smile" style="font-size: 12px; color: green;"> Positive</i>';  // Font Awesome icon for positive sentiment
        case 'negative':
            return  '<i class="fas fa-frown" style="font-size: 12px; color: red;"> Negative</i>';  // Font Awesome icon for negative sentiment
        case 'neutral':
            return  '<i class="fas fa-meh" style="font-size: 12px; color: blue;"> Neutral</i>';  // Font Awesome icon for neutral sentiment
        default:
            return '';  // No icon
    }
}