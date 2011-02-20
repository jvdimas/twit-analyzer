#!/usr/bin/env python
import sys, os, datetime
import sqlite3
import matplotlib.pyplot as plt

import TweetAnalyzer

def main(*args):
  analyzer = TweetAnalyzer.TweetAnalyzer()
  scores = []
  t = 60 # seconds

  # Find all db files available...
  dbList = os.listdir('db')

  for db_name in dbList:
    # Ignore files that are not databases...
    if not db_name.endswith('.db'):
      continue
    
    # Open the db
    print "Opening " + db_name + "...",
    conn = sqlite3.connect('db/' + db_name)
    c = conn.cursor()

    # Get all tweets and their scores
    c.execute('SELECT * from tweets')
    for t in c:
      scores.append((t[2], analyzer.score_tweet(t))) # append date,score

    print "done."
  
  print "Analyzing..."
  score_dict = {} # dictionary containing scores for each time period
  # Analyze date,score pairs to get aggregate score for each time period
  for s in scores:
    # Get datetime timestamp for score
    dt = datetime.datetime.strptime(s[0], "%Y-%m-%d %H:%M:%S")
    
    try:
      score_dict[format_dt(dt)].append(s[1])
    except:
      score_dict[format_dt(dt)] = [s[1],]

  x_pts = []
  y_pts = []
  for t in score_dict:
    #print t + ": " + str(analyzer.average_scores(score_dict[t]))
    y_pts.append(analyzer.average_scores(score_dict[t]))
    x_pts.append(t)

  plt.plot(y_pts)
  plt.xlabel('minute')
  plt.ylabel('number of tweets')
  plt.show()

def format_dt(dt):
  return dt.strftime("%Y-%m-%d %H:%M")

if __name__ == '__main__':
  try:
    sys.exit(main(*sys.argv))
  except KeyboardInterrupt:
    print "Exiting"
