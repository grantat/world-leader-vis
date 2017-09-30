#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import json
from os import getenv
try:
    from config import setEnvironVars
except Exception:
    print("There is no config file")


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3200 tweets with this
    # method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed
    # count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    saveCSV(alltweets, screen_name)
    save_backupJson(alltweets, screen_name)


def saveCSV(alltweets, screen_name):
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at,
                  tweet.text.encode("utf-8")]
                 for tweet in alltweets]
    with open('data/%s_tweets.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)


def save_backupJson(alltweets, screen_name):
    '''
    In case the data saved to csv for presentation is not enough,
    backup entire json response from twitter. Not to be stored in
    public repository
    '''
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [tweet._json
                 for tweet in alltweets]
    with open('data/backup_json/%s_tweets.json' % screen_name, 'w') as f:
        json.dump(outtweets, f)


def loadTwitterNames():
    print


if __name__ == '__main__':
    # setup environment variables
    setEnvironVars()
    # The keys for the Twitter app we're using for API requests
    access_key = getenv("TWITTER_ACCESS_TOKEN")
    access_secret = getenv("TWITTER_ACCESS_TOKEN_SECRET")
    consumer_key = getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = getenv("TWITTER_CONSUMER_SECRET")

    twitterNamesFile = "data/twitterNames.txt"
    get_all_tweets("realDonaldTrump")
