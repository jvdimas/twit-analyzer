# This is an extremely primitive attempt at assigning a score to a tweet that is
# supposed to convey to what degree it is positive or negative. General Inquirer
# is a project that produced lists of words classified by different
# emotions/states. Here I loook at just two of those: Positive and Negative.
# Analysis is just done on the frequency of word use: no attempt is made to
# correct for anything else that may be conveyed by usage or grammar.

# ToDo: Investigate using NLTK package to create something that, well, doesn't
# suck so much

import TweetAnalyzer

class AnalyzerGeneralInq(TweetAnalyzer.TweetAnalyzer):
  def __init__(self):
    # Construct two lists from general_inquirer txt files
    # One contains words with claimed positive connotations, the other words with
    # claimed negative connotations
    # ToDo: use more efficient data structure (Trie?)
    self.pos = []
    self.neg = []

    # With block to ensure file closed properly
    # ToDo: currently only works if used in a script invoked from root directory
    # of source tree
    with open('analyzers/general_inquirer/TAGPos.txt', 'r') as f:
      pos = f.readlines()
      for line in pos:
        self.pos.append(line.split(None, 1)[0]) # Process string to append just word

    with open('analyzers/general_inquirer/TAGNeg.txt', 'r') as f:
      neg = f.readlines()
      for line in neg:
        self.neg.append(line.split(None, 1)[0])

  def score_tweet(self, tweet):
    score = 0
    # ToDo: This won't catch all nonenglish tweets. Find a better way
    if tweet[4] == 'en':
      words = tweet[1].split(None)
      for w in words:
        w = w.upper() # pos and neg lists are all uppercase 
        if self.pos.count(w) > 0:
          score += 1
        if self.neg.count(w) > 0:
          score -= 1
      return score
    else:
      return 0

  def average_scores(self, scores):
    n = len(scores)
    if n == 0:
      return 0
    else:
      return float(sum(scores))/n 
