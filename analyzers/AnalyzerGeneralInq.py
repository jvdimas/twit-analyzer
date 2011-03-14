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
    # Construct two tries from general_inquirer txt files
    # One contains words with claimed positive connotations, the other words with
    # claimed negative connotations
    # ToDo: currently only works if used in a script invoked from root directory
    # of source tree
    self.pos = build_trie('analyzers/general_inquirer/TAGPos.txt')
    self.neg = build_trie('analyzers/general_inquirer/TAGNeg.txt')

  def score_tweet(self, tweet):
    score = 0
    # ToDo: This won't catch all nonenglish tweets. Find a better way
    if tweet[4] == 'en':
      words = tweet[1].split(None)
      for w in words:
        w = w.upper() # pos and neg lists are all uppercase 
        if self.pos.find(w):
          score += 1
        if self.neg.find(w):
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

# Given a path to a General Inquirer file builds a trie with the contained words
def build_trie(filepath):
  t = Trie() # new trie
  # with block ensures file is closed properly
  with open(filepath) as f:
    lines = f.readlines()
    for l in lines:
      word = l.split(None, 1)[0] # only want first word of each line
      t.add(word)
  return t

# Implementation of Trie
# Used to store words in the general inq db
# Faster than storing the words in a list
# Modified version of James Tauber's implementation
# http://jtauber.com/
class Trie(object):
  def __init__(self):
    self.root = [False, {}]

  # Adds key to the trie
  def add(self, key):
    curr_node = self.root
    for ch in key:
      curr_node = curr_node[1].setdefault(ch, [False, {}])
    curr_node[0] = True

  # Returns true if key is in the trie, false otherwise
  def find(self, key):
    curr_node = self.root
    for ch in key:
      try:
        curr_node = curr_node[1][ch]
      except KeyError:
        return False
    return curr_node[0]
