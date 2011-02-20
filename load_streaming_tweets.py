#!/usr/bin/env python

import sys, os
import subprocess
import pickle

# version of tweepy installed has some issues in Streaming fixed here
from lib.streaming import StreamListener, Stream 
import tweepy # Twitter API class: http://github.com/joshthecoder/tweepy

# StreamListener to import tweets into db
import StreamWatcherMongoDB
import StreamWatcherSQLite
import settings

def main(*args):
  print "Attempting to authorize with Twitter"
  # Attempt to authorize app with Twitter
  auth = tweepy.OAuthHandler(settings.CONSUMER_TOKEN, settings.CONSUMER_SECRET) # app keys
  # Consumer keys, these are user specific
  auth.set_access_token(settings.ACCESS_TOKEN_KEY, settings.ACCESS_TOKEN_SECRET)  

  # Infinite loop so connection is reestablished in case of network error
  while True:
    try:
      # Ensure authorization is valid...
      api = tweepy.API(auth)
      api.home_timeline(count = 1)
      
      # Start litsenting to the stream...
      listen_to_stream(auth)
    except tweepy.error.TweepError: # authorization failure
      auth = authorize_user(auth) # get user authorization key from Twitter
      listen_to_stream(auth) # now listen to the stream...
    
# Construct streaming object from auth and print infinite tweets
def listen_to_stream(auth):
  #listener = StreamWatcherMongoDB.StreamWatcherMongoDB()
  listener = StreamWatcherSQLite.StreamWatcherSQLite()
  stream = Stream(auth, listener)
  print "Sampling Stream..."
  stream.sample()

def authorize_user(auth):
  print "No valid authorization details found. Opening browser window..."
  
  auth_url = auth.get_authorization_url()
  print "If no window opens please go to: %s" % auth_url
  p = subprocess.Popen("open %s" % auth_url, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
  
  verifier = raw_input("What's your PIN: ").strip()
  print "Requesting access token..."
  auth.get_access_token(verifier)
  
  print "Saving auth details..."
  pickle.dump( (auth.access_token.key, auth.access_token.secret),
              open('settings_twitter_creds', 'w'))
  return auth

if __name__ == '__main__':
  try:
    sys.exit(main(*sys.argv))
  except KeyboardInterrupt:
    print "Exiting"
