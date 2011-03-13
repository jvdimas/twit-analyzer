# Base implementation of TweetAnalyzer
# All other TweetAnalyzer implementations should be children of this class
class TweetAnalyzer(object):
  # Assign all tweets score 1
  def score_tweet(self, tweet):
    return 1

  # Just return the sum
  def average_scores(self, scores):
    sum(scores)
