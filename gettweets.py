#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv
import json
from os import getenv, path
try:
    from config import setEnvironVars
except Exception:
    print("There is no config file")


def get_all_tweets(screen_name, api):
    # Twitter only allows access to a users most recent 3200 tweets with this
    # method

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum
    # allowed count)
    new_tweets = []
    try:
        new_tweets = api.user_timeline(
            screen_name=screen_name, count=200)
    except tweepy.TweepError:
        print("Could not get the following user's timeline:",
              screen_name)
        return

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

    # saveCSV(alltweets, screen_name)
    save_backupJson(alltweets, screen_name)


def saveCSV(alltweets, screen_name):
    """
    transform the tweepy tweets into a 2D array that will populate the csv
    """
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


if __name__ == '__main__':
    # setup environment variables
    setEnvironVars()
    # The keys for the Twitter app we're using for API requests
    access_key = getenv("TWITTER_ACCESS_TOKEN")
    access_secret = getenv("TWITTER_ACCESS_TOKEN_SECRET")
    consumer_key = getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = getenv("TWITTER_CONSUMER_SECRET")

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # check if I have the twitter users I want to check
    if(sum(1 for line in open('data/worldLeaders.json')) < 1):
        # Iterate through all members of the owner's list
        worldLeaderList = []
        for member in tweepy.Cursor(api.list_members, 'verified',
                                    'world-leaders').items():
            worldLeaderList.append(member._json)

        with open('data/worldLeaders.json', 'w') as f:
            json.dump(worldLeaderList, f)

    with open('data/worldLeaders.json', 'r') as f:
        # load users
        wl = json.load(f)

        for leader in wl:
            screen_name = leader["screen_name"]

            if path.isfile("data/" + screen_name + "_tweets.csv") or \
                    path.isfile("data/backup_json/" + screen_name +
                                "_tweets.json"):
                continue

            get_all_tweets(screen_name, api)
