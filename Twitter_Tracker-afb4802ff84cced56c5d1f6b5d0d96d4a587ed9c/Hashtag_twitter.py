import sys
import tweepy
import json
import pickle
import os
import operator
import argparse
import time
import datetime


CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

hashtag_to_track = '#trump'
participant = {}
filename = 'output.p'
global start
start = time.time()

if not os.path.exists("log"):
    os.makedirs("log")


def loadData():
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            global participant
            participant = dict(pickle.load(f))


def parseArgs():
    parser = argparse.ArgumentParser("Hashtag tracker using Twitter Stream api")
    parser.add_argument('-x', help="Hashtag to track", dest="hashtag_to_track")
    args = parser.parse_args()
    return args


def writeToLog(sorted_participants):
    filename = "log/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".log"
    with open(filename, 'w+') as f:
        f.write("User, Count")
        f.write('\n\n')
        f.write('\n'.join('%s %s' % x for x in sorted_participants))
        f.write('\n')


class MyStreamListener(tweepy.StreamListener):
    def on_disconnect(self, notice):
        print
        notice

    def on_connect(self):
        print
        "Stream API Connected"

    def on_error(self, status):
        print
        status

    def on_status(self, status):
        status = json.dumps(status._json)
        status = json.loads(status)

        name = status[u'user'][u'screen_name']  # name
        tweet_hashtag_list = status[u'entities'][u'hashtags']  # list of dict

        if not name in participant.keys():
            for hash_dict in tweet_hashtag_list:
                if ("#" + hash_dict[u'text']).lower() == hashtag_to_track:
                    participant[name] = 1
        else:
            participant[name] += 1

        print
        "**************"
        sorted_participants = sorted(participant.items(), key=operator.itemgetter(1), reverse=True)
        print
        sorted_participants
        print
        "**************"
        pickle.dump(sorted_participants, open(filename, "wb"))
        end = time.time()

        global start
        if (end - start > 900):
            writeToLog(sorted_participants)
            start = time.time()


if __name__ == "__main__":

    args = parseArgs()

    if args.hashtag_to_track:
        hashtag_to_track = args.hashtag_to_track

    try:
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
    except:
        sys.exit("Error: Unable to authenticate")

    loadData()

    try:
        myStream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
        myStream.filter(track=[hashtag_to_track])
    except Exception as e:
        myStream.disconnect()
        print
        str(e)
        sys.exit("Twitter stream disconnected")