#!/usr/bin/python
import sys
import lib.mongodb # mongo db
import settings


def main(*args):
  print "Attempting to establish connection to database..."
  db = lib.mongodb.connect(settings.DB_NAME)
  tweets = db[settings.DB_NAME]
  count = tweets.find({'analyzed': False}).count()
  print count
  
  while count > 0:
    t = tweets.find_one({'analyzed': True})
    if t:
      t['analyzed'] = False
      tweets.save(t)
    count -= 1
    

if __name__ == '__main__':
  try:
    sys.exit(main(*sys.argv))
  except KeyboardInterrupt:
    print "Exiting"