import os
import json
import re
from textblob import TextBlob
# from textblob.sentiments import NaiveBayesAnalyzer
from bs4 import BeautifulSoup


def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])"
                           "|(\w+:\/\/\S+)", " ", tweet).split())


def get_sentiment(text):
    blob = TextBlob(clean_tweet(text))
    return blob.sentiment.polarity


def dump_sentiment():
    for filename in os.listdir("data/translations/"):
        username = filename[:-4]
        if filename.endswith(".htm"):
            print(filename)
            with open("data/translations/" + filename) as f, \
                    open("data/sentiment/" + username + ".json", 'w') as out:
                doc = f.read()
                temp = {}
                soup = BeautifulSoup(doc, 'html.parser')
                # take text from html that was translated
                for tag in soup.find_all("div", {"class": "tweets-text"}):
                    print(tag.get("id"), "|", tag.text)
                    text = tag.text.rstrip()
                    sentiment = get_sentiment(text)
                    temp[tag.get("id")] = {"text": text,
                                           "sentiment": sentiment}
                json.dump(temp, out)


if __name__ == "__main__":
    dump_sentiment()
