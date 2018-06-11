import twitter
import json
import random


with open('credentials.json') as f:
    credentials = json.loads(f.read())

api = twitter.Api(**credentials)

#status = api.PostUpdate('Can you hear me?')
try:
    status = api.PostUpdate('I can hear you!')
except UnicodeDecodeError:
    print("Your message could not be encoded.  Perhaps it contains non-ASCII characters? ")
    print("Try explicitly specifying the encoding with the --encoding flag")
    sys.exit(2)
	
def lambda_handler(_event_json, _context):
    tweets = poem_tweets()