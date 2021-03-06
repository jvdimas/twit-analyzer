import TweetAnalyzer

class AnalyzerPercentEnglish(TweetAnalyzer.TweetAnalyzer):
  def score_tweet(self, tweet):
    if tweet[4] == 'en':
      return 1
    else:
      return 0

  def average_scores(self, scores):
    n = 0
    n_en = 0
    for s in scores:
      n += 1
      n_en += s
    
    if n == 0:
      return 0
    else:
      return float(n_en)/n
