# World Leader Viz

The goal of this project is to visualize world leader social interactions collected from twitter. The names of the users used in this project were collected from the "[World Leaders](https://twitter.com/verified/lists/world-leaders/members?lang=en)" members list verified by Twitter, with the addition of other world leaders not currently in that list. For example Donald Trump (@realDonaldTrump) and Vladim

The goal of this project is to create a timeline of tweets from all of these users over time shown on a map. The hope, is that by the completion of this project there will be a map with a timeline that users can distinctly see: what twitter users were tweeting at the time, their sentiment at the time, the location a user is tweeting from, the location a user could possibly be talking about and/or a user that one user speaks about at a given time.

The data for these visualizations will be derived from techniques such as: sentiment analysis, clustering, and named-entity recognition.

## Possible Issues

The data is coming from Twitter's API. Twitter only allows the retrieving of the [last 3200 tweets](https://dev.twitter.com/rest/reference/get/statuses/user_timeline) from a user, assuming they even have 3200 tweets.

Twitter also has rate limits for using their API of 900 requests per 15 minutes. Fortunately we can collect 200 tweets per request. Assuming there are 70 users and 3200 tweets per user then: (70*3200)/200 = 1120 requests so this at least 15 minutes of requests.

This data is from different World leaders. Therefore, there will be more than one language involved in these tweets. To compensate for this, any language other than English, will be converted to english and then tested upon. This can and probably will lead to noisy text which will lead to error in sentiment analysis.

## Private world leader twitters

- bluehousekorea

## Todo

1. [ ] Twitter Data collection
2. [ ] Data parsing
	- [ ] Text Translation
	- [ ] Sentiment analysis
	- [ ] Location or person speech is directed at
3. [ ] Visualizations
	- [ ] World Map
	- [ ] Sentiment clustering
	- [ ] Postive/negative sentiment bar

## Tools

- Google translate
- Tweepy(Twitter SDK)
- D3.js
