import pickle

###############################
# Settings
###############################
# App-Specific
CONSUMER_TOKEN = "Ev7Rv3mS9liUCeIgEcYYw"
CONSUMER_SECRET = "mwRSnOQZpsH5uct017ATlOPSbVLD2UCkOG1Fc3ntuMc"

# MongoDB name
DB_NAME = "tweets"

# User specific twitter auth details
try:
  (ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET) = pickle.load(open('settings_twitter_creds'))
except IOError:
  (ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET) = ('', '')
