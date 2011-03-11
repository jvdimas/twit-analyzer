#!/usr/bin/env python
import sys, os, datetime
import sqlite3
import matplotlib.pyplot as plt
import csv

import analyzers.TweetAnalyzer as TweetAnalyzer
import analyzers.AnalyzerPercentEnglish as AnalyzerPercentEnglish

def main(*args):
  analyzer = TweetAnalyzer.TweetAnalyzer()
  #analyzer = AnalyzerPercentEnglish.AnalyzerPercentEnglish() 
  scores = []

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

  # Now write csv info to file...
  print "Writing csv to file 'out.csv'"
  writer = csv.writer(open("out.csv", "wb+"))
  writer.writerow( ('date', 'score') )
  for t in score_dict:
    writer.writerow( date, score_dict[date] )

def format_dt(dt):
  return dt.strftime("%Y-%m-%d %H:%M") # ("%Y-%m-%d %H:%M")

if __name__ == '__main__':
  try:
    sys.exit(main(*sys.argv))
  except KeyboardInterrupt:
    print "Exiting"
