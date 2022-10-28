import pygi
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob

class TwitterClient(object) : 
	
	def __init__(self): 
		
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'xxxxxxxx'
		consumer_secret = 'xxxxxx'
		access_token = 'xxxxxxxx'
		access_token_secret = 'xxxxxxx'

		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 100): 
		
		tweets = [] 

		try: 
			fetched_tweets = self.api.search(q = query, count = count) 

			for tweet in fetched_tweets: 
				parsed_tweet = {} 

				parsed_tweet['text'] = tweet.text 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				if tweet.retweet_count > 0: 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			return tweets 

		except tweepy.TweepError as e: 
			print("Error : " + str(e)) 


class MainWindow(Gtk.Builder):
    def __init__(self, builder):
        builder = builder
    def on_b1_clicked(self, b1):
        text = builder.get_object("c1")
        query = text.get_text()
	tweets = api.get_tweets(query, count = 2000)
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
	print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) 

	print("\n\nPositive tweets:") 
	for tweet in ptweets[:10]: 
		print(tweet['text']) 

	print("\n\nNegative tweets:") 
	for tweet in ntweets[:10]: 
		print(tweet['text'])     
api = TwitterClient() 	 
builder = Gtk.Builder()
builder.add_from_file("beat.glade")
query = "None"
window = builder.get_object("mainwin")
window.show_all()
window.connect("delete_event", Gtk.main_quit)
builder.connect_signals(MainWindow(builder))	

Gtk.main()	