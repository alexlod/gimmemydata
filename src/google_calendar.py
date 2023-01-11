import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

# replace with the path to your service account key
SERVICE_ACCOUNT_FILE = 'path/to/service_account_key.json'

# specify the date range for which you want to retrieve events
start_date = datetime.datetime(2022, 1, 1)
end_date = datetime.datetime(2022, 12, 31)

# initialize the calendar service
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
service = build('calendar', 'v3', credentials=credentials)

# call the calendar.events.list method to retrieve events within the specified date range
events_result = service.events().list(calendarId='primary', timeMin=start_date.isoformat()+'Z',timeMax=end_date.isoformat()+'Z', singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])

# print the summary and start time of each event
if not events:
    print('No events found.')

for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(event['summary'] + ' on ' + start)
