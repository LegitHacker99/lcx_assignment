from os import getenv
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

class config:
    RSS_URL = getenv("RSS_URL", "http://rss.cnn.com/rss/cnn_topstories.rss")
    POLLING_INTERVAL = getenv("POLLING_INTERVAL", 600)
    MODEL_REPO_ID = getenv("model_repo_id", "microsoft/Phi-3.5-mini-instruct")
    HF_KEY = getenv("HF_KEY")
