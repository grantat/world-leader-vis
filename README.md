# World Leader Visualization

The goal of this project is to visualize world leader social interactions collected from twitter.
The names of the users used in this project were collected from the "[World Leaders](https://twitter.com/verified/lists/world-leaders/members?lang=en)" members list verified by Twitter, with the addition of other world leaders not currently in that list.

The goal of this project is to create a timeline of tweets from all of these users over time shown on a map.
The hope, is that by the completion of this project there will be a map with a timeline that users can distinctly see: what twitter users were tweeting at the time, their sentiment at the time, the location a user is tweeting from, the location a user could possibly be talking about and/or a user that one user speaks about at a given time.

The data for these visualizations will be derived from techniques such as: sentiment analysis, clustering, and named-entity recognition.

## Possible Issues

The data is coming from Twitter's API.
Twitter only allows the retrieving of the [last 3200 tweets](https://dev.twitter.com/rest/reference/get/statuses/user_timeline) from a user, assuming they even have 3200 tweets.

Twitter also has rate limits for using their API of 900 requests per 15 minutes.
Fortunately we can collect 200 tweets per request. Assuming there are 70 users and 3200 tweets per user then: (70*3200)/200 = 1120 requests so this at least 15 minutes of requests.

This data is from different World leaders. Therefore, there will be more than one language involved in these tweets.
To compensate for this, any language other than English, will be converted to english and then tested upon. This can and probably will lead to noisy text which will lead to error in sentiment analysis.

## Private world leader twitters

- [bluehousekorea](https://twitter.com/bluehousekorea)

## Todo

1. [x] Twitter Data collection
2. [x] Data parsing
	- [x] Text Translation
	- [x] Sentiment analysis
	- [ ] ~~Location or person speech is directed at~~
3. [x] Visualizations
	- [x] ~~World Map~~ Heatmap of tweet times per month
	- [x] ~~Sentiment clustering~~ Term usage among users
	- [x] Postive/negative sentiment bar

## Tools

- Google translate
- Tweepy(Twitter SDK)
- beautifulsoup4
- textblob
- nltk
- D3.js

Google translate and D3.js are used in separate parts of processing data.
The other four requirements however can be installed using pip with the following command:

```shell
$ pip3 install -r requirements.txt
```

## Data Notes

First I got all the tweets from the leaders I needed.
I saved each of the JSON responses in backup_json.
I then transformed each of the text from each tweet into an HTML page.
This avoided the need for me to pay for Google Translate by simply going to web page and allowing google to detect a foreign language.
If the language was english it was not converted in anyway.
If a language worked on a majority of the tweets but could not translate a few of them I simply discarded them.
This proved true for the following users:
- @eucopresident
- @QueenNoor

If a language could not be detected by Google for all of the tweets, the user would be discarded.
This only proved true for the following users:
- @YLeterme who used 6 different languages

MedvedevRussia is MedvedevRussiaE in english.
I simply took the english version.

There were 272 tweets at the same datetime.
Therefore, the tweets had to be chunked in groups on that same datetime:

```Javascript
{
	12314121251: [{"tweet1": 123}, {"tweet2": 234}],
}
```

There were 63 users in the end.
There were 165553 unique timestamps for all tweets with a total of 165799 overall.
The timeframe will be anytime before October 3rd.
These were then grouped if they had the same day.

I created date ranges on based on the number of tweets.
If a date range had atleast 100 tweets I would mark that as a range.
For example, if October 2, 2017 had 355 tweets it would have its own standalone date stamp.
However, if a date had only 50 tweets it would keep going back until there were at least 100 in the date range.
One example of this is September 30 - October 1, 2017 would go beyond 100 tweets therefore two dates are in that date range.

## Testing Locally

To test this application on a server, assuming you have python installed, perform the following commands:

```
$ cd app
$ python -m SimpleHTTPServer 8000
```

Then navigate to http://localhost:8000.
Make sure none of your plugins can block requests made by d3.
If you have an ad-block installed, its recommended to disable it for localhost.
