"""
Web Scraping with Requests + BeautifulSoup, then a Word Cloud
---------------------------------------------------------------
Course: NLP Assignment
Goal:
  1. Download the HTML content of https://www.python.org
  2. Use BeautifulSoup to extract the visible page text
  3. Clean the text and remove stop words
  4. Build a word cloud from what's left, using the `wordcloud` module
"""

import re
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords

# ---------------------------------------------------------------
# STEP 0: Make sure NLTK's stopword list is available locally.
#         (only downloads the first time you run this)
# ---------------------------------------------------------------
nltk.download("stopwords", quiet=True)

def fetch_page(url):
    """
    STEP 1: Download the raw HTML of the target webpage.
    Returns the HTML as a string, or raises an error if the request fails.
    """
    headers = {"User-Agent": "Mozilla/5.0 (educational NLP scraping assignment)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # stop early if the page didn't load (e.g. 404, 500)
    return response.text

def extract_text(html):
    """
    STEP 2: Use BeautifulSoup to pull the human-readable text out of the HTML,
    throwing away tags, scripts, and style blocks (which aren't real "words").
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove elements that hold no readable prose
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    return text

def clean_and_remove_stopwords(text):
    """
    STEP 3:
      a) Lowercase everything
      b) Keep only alphabetic tokens (strip numbers/punctuation/symbols)
      c) Remove English stop words (the, is, and, ...) using NLTK's list
    Returns a single space-joined string of the surviving words,
    which is the input format the WordCloud generator expects.
    """
    # a) lowercase
    text = text.lower()
    # b) tokenize: find sequences of letters only, length > 1 (drops single letters/junk)
    words = re.findall(r"[a-z]{2,}", text)
    # c) remove stop words
    stop_words = set(stopwords.words("english"))
    # A few extra web/boilerplate words that aren't in NLTK's list but
    # clutter up scraped site text; adjust/trim this as you like.
    extra_stopwords = {"python", "org"}  # comment this line out if you WANT "python" in the cloud
    filtered_words = [
        w for w in words if w not in stop_words and w not in extra_stopwords
    ]
    return " ".join(filtered_words)

def make_wordcloud(text, output_path="wordcloud.png"):
    """
    STEP 4: Feed the cleaned text into WordCloud, render it with matplotlib,
    and save it to a PNG file.
    """
    wc = WordCloud(
        width=1200,
        height=800,
        background_color="white",
        colormap="viridis",
        max_words=150,
    ).generate(text)
    plt.figure(figsize=(12, 8))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Word cloud saved to {output_path}")

def main():
    url = "https://www.python.org"
    print(f"Fetching {url} ...")
    html = fetch_page(url)
    print("Extracting text with BeautifulSoup ...")
    raw_text = extract_text(html)
    print("Cleaning text and removing stop words ...")
    cleaned_text = clean_and_remove_stopwords(raw_text)
    print(f"Word count after cleaning: {len(cleaned_text.split())}")
    print("Building word cloud ...")
    make_wordcloud(cleaned_text)


if __name__ == "__main__":
    main()
