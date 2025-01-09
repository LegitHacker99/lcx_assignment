import time
from tqdm import tqdm
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request

from app.fetch_article import poll_rss_feed
# from app.caption_generator import generate_caption
from app.media_generator import generate_image
from app.utils import shorten_url
from app.llm_query import generate_caption_with_llm as generate_caption

from config import config
from logger import logging

app = Flask(__name__)

app.config['IMAGE_FOLDER'] = os.path.join(os.getcwd(), 'static', 'images')

def process_article(article):
    """ 
    Process each article: generate caption, shorten URL, and save image. 

    Args:
        article (dict): The article dict.
        
    Returns:
        TBD
    """
    caption = generate_caption(article.get("content")) if article.get("content") else None
    # caption = generate_caption(article) if article else None
    short_url = shorten_url(article['url'])
    image = generate_image(article.get("content")) if article.get("content") else None

    logging.info(f"Processing article: {article['title']}")
    logging.info(f"Caption: {caption}")
    logging.info(f"Shortened URL: {short_url}")
    
    if image:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Hash the URL to create a short unique string (for safety if URL is very long)
        url_hash = hashlib.md5(article['url'].encode()).hexdigest()[:8]
        image_filename = f"generated_image_{url_hash}_{timestamp}.png"
        image.save(image_filename)

def fetch_and_process_articles(url, seen_articles):
    """ 
    Poll the RSS feed and process new articles. 

    Args:
        url (str): RSS url for polling
        seen_articles (set): set for checking if the article has been processed earlier
        
    Returns:
        bool: if new articles found
    """
    articles = poll_rss_feed(url)
    new_articles = []

    # Check for new articles by comparing the URL with the seen articles
    for article in tqdm(articles, desc="Checking for new articles"):
        if article.get('url') not in seen_articles:
            seen_articles.add(article['url'])
            new_articles.append(article)
            print(f"New article found: {article['title']}\n", flush=True)

    if new_articles:
        # process_article(new_articles[0]['title'])
        for article in new_articles:
            process_article(article)

    return len(new_articles) > 0  # Return True if new articles were found and processed

def main():
    url = config.RSS_URL
    polling_interval = config.POLLING_INTERVAL
    seen_articles = set()  # Keep track of seen URLs to avoid duplicate fetching
    
    while True:
        try:
            # Fetch and process new articles if they exist
            new_articles_found = fetch_and_process_articles(url, seen_articles)

            if not new_articles_found:
                logging.info(f"No new articles found, retrying in {polling_interval} secs...")
            else:
                logging.info("Processed new articles successfully.")
            
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)

        # Wait for the next polling cycle
        time.sleep(polling_interval)

if __name__ == "__main__":
    main()
