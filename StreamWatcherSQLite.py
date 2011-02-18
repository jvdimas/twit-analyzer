# New implementation of StreamWatcher
# Stores data in an SQLite database, rotated daily

import time
import datetime

import sqlite3

# version of tweepy installed has some issues in Streaming fixed here
import lib.streaming
import tweepy
# import tweepy # Twitter API class: http://github.com/joshthecoder/tweepy

import settings
import pw # temporary password file... 

# StreamListener class implementation 
# Listens to live feed of tweets loading them into the mongo db 
class StreamWatcherSQLite(lib.streaming.StreamListener):
  def __init__(self, api=None):
    self.api = api or tweepy.API()
    
    self.count = 0 # number of tweets loaded into db in last 60 seconds
    self.start_time = 0 #time execution starts, resets every 60 seconds
    
    self.initialize_db() # setup the db

  # Initialize db
  def initialize_db(self):
    # Open db connection
    self.db = sqlite3.connect(self.get_db_name())    
    self.cursor = self.db.cursor()
    self.day = datetime.datetime.now().day

    # Create db tables
    self.create_tables()

  # Creates db tables
  def create_tables(self):
    try:
      print "Creating database...",
      cmd = "CREATE TABLE tweets(author TEXT, text TEXT, created_at TIMESTAMP, geo TEXT, user_lang TEXT)"
      self.cursor.execute(cmd)
      self.db.commit()
      print "done."
    except:
      print "already exists"

  # Tweet recieved from live stream...
  def on_status(self, tweet):
    # if time is 0 count has just begun
    if self.start_time == 0:
      self.start_time = time.time()
    if time.time() - self.start_time > 60:
      self.start_time = time.time()
      print "%d tweets recieved in the last minute." % self.count
      self.count = 0

      # Now check to see if a day is elapsed
      # If one has we need to rotate into a new db file
      if datetime.datetime.now().day != self.day:
        self.day = datetime.datetime.now().day
        self.initialize_db() 
       
    #insert into db
    try:
      cmd = """INSERT INTO tweets(author, text, created_at, geo, user_lang) VALUES ("%s",
      "%s", "%s", "%s", "%s")""" % (tweet.author.screen_name, tweet.text,
      tweet.created_at, tweet.geo, tweet.author.lang)

      self.cursor.execute(cmd)
      self.db.commit()
      self.count += 1
    except:
      # Ignore any unicode errors...
      pass
    return True
  
  def on_error(self, status_code):
    print 'An error has occured! Status code = %s' % status_code
    return True  # keep stream alive
  
  def on_timeout(self):
    print 'Timeout...'
    self.start_time = 0
    return False

  # Returns name to use for the db
  # Changes based on current date
  def get_db_name(self):
    now = datetime.datetime.now()
    return "db/tweets-%s-%s-%s.db" % (now.year, now.month, now.day) 
