import tweepy
import csv
from textblob import TextBlob

import numpy as np
import operator


# Step 1 - Authenticate
consumer_key= ''
consumer_secret= ''


access_token=''
access_token_secret=''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# Step 2 - Prare Query
# List of state leaders
politicians_names = ['Putin', 'Trump', 'Poroshenko', 'Merkel']
# tag related to event
name_of_event = 'HelsinkiSummit'

# Label for analysis
def get_labed(analysis, threshold_up = 0.15, threshold_low = -0.1):
	if analysis.sentiment[0] > threshold_up:
		return 'Positive'
	elif analysis.sentiment[0] < threshold_low:
		return 'Negative'
	else:
		return  'Neutral'

# Step 3 - Saving Tweets
all_polarities = dict()
for politician in politicians_names:
	this_politician_polarities =[]
	this_politician_tweets = api.search(q=[name_of_event, politician], count=100)
	with open('%s_tweets.csv' % politician, 'wb') as this_politician_file:
		this_politician_file.write('tweet, sentiment_label[0]\n')
		for tweet in this_politician_tweets:
			analysis = TextBlob(tweet.text)
			# Get label for this sentiment analysis
			this_politician_polarities.append(analysis.sentiment[0])
			this_politician_file.write('%s,%s\n' % (tweet.text.encode('utf-8'), get_labed(analysis)))
	# Save mean for a result
	all_polarities[politician] = np.mean(this_politician_polarities)
    
# Step 4 - print a result
sorted_analysis = sorted(all_polarities.items(), key=operator.itemgetter(1), reverse=True)
print 'Mean Sentiment Polarity in descending order :'
for politician, polarity in sorted_analysis:
	print '%s : %0.2f' % (politician, polarity)