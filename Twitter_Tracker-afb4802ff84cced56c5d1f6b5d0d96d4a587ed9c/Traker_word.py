import tweepy
import sys
import pymongo

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
	def __init__(self, api):
		self.api = api
		super(tweepy.StreamListener, self).__init__()

		self.db = pymongo.MongoClient().Ebolag

	def on_status(self, status):
		print(status.text, "\n")

		data = {}
		data['text'] = status.text
		data['created_at'] = status.created_at
		data['geo'] = status.geo
		data['source'] = status.source

		self.db.Tweets.insert(data)

	def on_error(self, status_code):
		print >> sys.stderr, "error with status code:", status_code
		return True

	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True

track = tweepy.streaming.Stream(auth, CustomStreamListener(api))
track.filter(track=['Trump'])