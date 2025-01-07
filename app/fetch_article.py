import feedparser
from newspaper import Article
from tqdm import tqdm

from logger import logging

# Fetch the article text using the newspaper package
def fetch_article(url: str) -> str:
    article = Article(url)

    try:
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        logging.error(f"Error downloading article: {e}", exc_info=True)
        return ""

def fetch_latest_articles(rss_url: str):
    feed = feedparser.parse(rss_url)
    articles = []
    
    for entry in feed.entries:
        title = entry.get("title", None)
        url = entry.get("link", None)
        published = entry.get("published", None)
        
        print(f"Title: {title}", flush=True)
        print(f"URL: {url}", flush=True)
        print(f"Published: {published}", flush=True)
        
        # Fetch article content using newspaper
        article_text = fetch_article(url)
        if not article_text and entry.get("summary", None):
            article_text = entry.get("summary", None)

        # print(f"Article Text: {article_text[:200]}...", flush=True)
        print("\n" + "="*120 + "\n", flush=True)
        
        articles.append({"title": title, "url": url, "published": published, "content": article_text})
    
    return articles

def poll_rss_feed(rss_url: str):
    return fetch_latest_articles(rss_url)
