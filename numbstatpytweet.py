from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from google.oauth2 import service_account
import googleapiclient.discovery
import sys
import twitter
import json
import random



def get_events():
	# Setup the Calendar API
	SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
	SERVICE_ACCOUNT_FILE = 'service.json'

	credentials = service_account.Credentials.from_service_account_file(
			SERVICE_ACCOUNT_FILE, scopes=SCOPES)

	service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

	# Call the Calendar API
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print('Getting the upcoming 10 events')
	events_result = service.events().list(calendarId='nfte4cs4mhli31ifbn8tg81pa8@group.calendar.google.com', timeMin=now,
										  maxResults=4, singleEvents=True,
										  orderBy='startTime').execute()
	events = events_result.get('items', [])
	return events

def build_tweet():
	#Initialize event collector
	events = get_events()
	responses = ''
	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	querytime = now.split("T")[1].split(".")
	responses += 'Next 4 Events: ' + querytime[0] + '\n'
	if not events:
		responses += str('No upcoming events found.')
	#start: '2018-06-07T06:20:00Z'
	#event['summary']: 'F06 13503kHz RTTY [Target: East Asia]'
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		bcast = start.split("T")
		responses += str(bcast[1] + ' ' + event['summary'] + '\n')
	return responses

def send_tweet():
	with open('credentials.json') as f:
		credentials = json.loads(f.read())
	api = twitter.Api(**credentials)
	contents = build_tweet()
	status = api.PostUpdate(contents) #'\n Listen: http://websdr.ewi.utwente.nl:8901/'

def lambda_handler(_event_json, _context):
    send_tweet()