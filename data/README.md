# Data

This directory contains all of the data and transformations applied to the data collected from twitter.
The following lists the directories in order from which they were created and the purpose of each:

1. `backup_json` - Initial collected tweets from each world leader with no modifications
2. `html` - All the tweets from each user and inserted into HTML documents
3. `translations` - All the html files for each user, excluding duplicates, translated into english HTML documents
4. `sentiment` - Sentiment calculations from the translated text for each user
5. `chunks` - Tweets separated into the months they were created containing: user tweet text, user sentiment, and tweet date time
6. `heatmap` - Tweet date times formatted in CSV files for Heatmap usage
7. `clusters` - Cluster data based on top-k terms of each month
