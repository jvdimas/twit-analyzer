import time

import lib.mongodb # mongo db

# version of tweepy installed has some issues in Streaming fixed here
import lib.streaming
import tweepy
# import tweepy # Twitter API class: http://github.com/joshthecoder/tweepy

import settings


# StreamListener class implementation 
# Listens to live feed of tweets loading them into the mongo db 
class StreamWatcherMongoDB(lib.streaming.StreamListener):
  
  def __init__(self, api=None):
    self.api = api or tweepy.API()
    
    self.count = 0 # number of tweets loaded into db in last 60 seconds
    self.start_time = 0 #time execution starts, resets every 60 seconds
    
    #open db connection
    self.db = lib.mongodb.connect(settings.DB_NAME)
  
  # Tweet recieved from live stream...
  def on_status(self, tweet):
    # if time is 0 count has just begun
    if self.start_time == 0:
      self.start_time = time.time()
    if time.time() - self.start_time > 60:
      self.start_time = time.time()
      print "%d tweets recieved in the last minute." % self.count
      self.count = 0
    
    self.count += 1
    
    # get tweet attributes
    t = {
      'author': tweet.author.screen_name,
      'contributors': tweet.contributors,
      'coordinates': tweet.coordinates,
      'created_at': tweet.created_at,
      # 'destroy': tweet.destroy,
      # 'favorite': tweet.favorite,
      'favorited': tweet.favorited,
      'geo': tweet.geo,
      'id': tweet.id,
      'in_reply_to_screen_name': tweet.in_reply_to_screen_name,
      'in_reply_to_status_id': tweet.in_reply_to_status_id,
      'in_reply_to_user_id': tweet.in_reply_to_user_id,
      # 'parse': tweet.parse,
      # 'parse_list': tweet.parse_list,
      'place': tweet.place,
      # 'retweet': dir(tweet.retweet),
      # 'retweets': dir(tweet.retweets),
      'source': tweet.source,
      # 'source_url': tweet.source_url,
      'text': tweet.text,
      'truncated': tweet.truncated,
      'user': tweet.user.screen_name,
      'user_lang': tweet.author.lang,
      'user_location': tweet.author.location,
      'user_statuses_count': tweet.author.statuses_count,
      'analyzed': False,
    }

    #insert into db
    try:
      #print self.DB_NAME
      self.db[settings.DB_NAME].insert(t)
    except:
      print "DB Insertion Error"
    return True
  
  def on_error(self, status_code):
    print 'An error has occured! Status code = %s' % status_code
    return True  # keep stream alive
  
  def on_timeout(self):
    print 'Timeout...'
    self.start_time = 0
    return False
