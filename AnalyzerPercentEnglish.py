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
      if s == 1:
        n_en += 1

    return float(n_en)/n
