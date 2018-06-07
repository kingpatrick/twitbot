from __future__ import print_function
import sys
import twitter
import json
import random
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from oauth2client import client
from googleapiclient import sample_tools

with open('credentials.json') as f:
    credentials = json.loads(f.read())
api = twitter.Api(**credentials)

service, flags = sample_tools.init(
        sys.argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar.readonly')

def numbstat_tweets():
	#Setup the Calendar API
	SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
	store = file.Storage('googlecredentials.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('calendar', 'v3', http=creds.authorize(Http()))

	# Call the Calendar API
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
	events_result = service.events().list(calendarId='nfte4cs4mhli31ifbn8tg81pa8@group.calendar.google.com', timeMin=now,
										  maxResults=5, singleEvents=True,
										  orderBy='startTime').execute()
	events = events_result.get('items', [])

	#Initialize event collector
	responses = ''
	if not events:
		responses += str('No upcoming events found.')
	#start: '2018-06-07T06:20:00Z'
	#event['summary']: 'F06 13503kHz RTTY [Target: East Asia]'
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		bcast = start.split("T")
		responses += str(bcast[1] + ' ' + event['summary'] + '\n')

	#Tweet any events or messages that were added to the responses list
	i = 0	
	#for i in range(len(responses)):
	#print('about to tweet: ' + responses)
	status = api.PostUpdate(responses) #'\n Listen: http://websdr.ewi.utwente.nl:8901/' )
	#i += 1

def lambda_handler(_event_json, _context):
    numbstat_tweets()

