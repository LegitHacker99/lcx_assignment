import pyshorteners

def shorten_url(url: str) -> str:
    s = pyshorteners.Shortener()
    return s.tinyurl.short(url)
