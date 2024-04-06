from flask import Flask,redirect,flash,render_template,request,url_for
import datetime
import os.path
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

# Google Calendar configuration
SERVICE_ACCOUNT_FILE = 'credentials.json'
CALENDAR_ID = 'primary'  # Use 'primary' for the primary calendar

# Load Google credentials
try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=credentials)
except FileNotFoundError:
    print("Service account credentials file not found. Make sure to create one.")

# Function to create a weekly event
def create_weekly_event(summary, description, start_time):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (start_time + datetime.timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'UTC',
        },
        'recurrence': ['RRULE:FREQ=WEEKLY;COUNT=10'],  # Repeat weekly for 10 occurrences
    }
    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event['id']

@app.route("/")
def index():
    start_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)  # Start meeting tomorrow
    summary = "Weekly Meeting by zyee"
    description = "This is a weekly meeting reminder."
    event_id = create_weekly_event(summary, description, start_time)
    return f"Meeting created! Event ID: {event_id}"



# @app.route('/', methods=["POST","GET"])
# def index():
    
#     if request.method == "POST":
#         try:
#             service = getService()
#             event = {
#             'summary': 'Google I/O 2015',
#             'location': '800 Howard St., San Francisco, CA 94103',
#             'description': 'A chance to hear more about Google\'s developer products.',
#             'start': {
#                 'dateTime': '2015-05-28T09:00:00-07:00',
#                 'timeZone': 'America/Los_Angeles',
#             },
#             'end': {
#                 'dateTime': '2015-05-28T17:00:00-07:00',
#                 'timeZone': 'America/Los_Angeles',
#             },
#             'recurrence': [
#                 'RRULE:FREQ=DAILY;COUNT=2'
#             ],
#             'attendees': [
#                 {'email': 'lpage@example.com'},
#                 {'email': 'sbrin@example.com'},
#             ],
#             'reminders': {
#                 'useDefault': False,
#                 'overrides': [
#                 {'method': 'email', 'minutes': 24 * 60},
#                 {'method': 'popup', 'minutes': 10},
#                 ],
#             },
#             }

#             event = service.events().insert(calendarId='primary', body=event).execute() # type: ignore
#             context = {"link":event.get('htmlLink')}
                    
            
#         except HttpError as error:
#             print(f"An error occurred: {error}")
    
#     return render_template('index.html')

# SCOPES = ['https://www.googleapis.com/auth/calendar']
# REDIRECT_URI = "https://calender-quf5.onrender.com/"


# """Shows basic usage of the Google Calendar API.
# Prints the start and name of the next 10 events on the user's calendar.
# """
# def getService():
#     token_file = 'token.pickle'
#     creds = None
#     if os.path.exists(token_file):
#         with open(token_file, 'rb') as token:
#             creds = pickle.load(token)
#     # creds = Credentials.from_authorized_user_file("token.json", SCOPES)

#     #If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = Flow.from_client_secrets_file("credentials.json", SCOPES,redirect_uri=REDIRECT_URI)
#             # Generate the authorization URL
#             authorization_url, state = flow.authorization_url(access_type='offline',
#                                                               include_granted_scopes='true')
#             # creds = flow.run_local_server(port=0)
#             return redirect(authorization_url)
            
            
#     # Save the credentials for the next run
#         with open(token_file, "wb") as token:
#             creds = flow.fetch_token(authorization_response=request.url)
#             pickle.dump(creds, token)
            
        
#         service = build("calendar", "v3", credentials=creds)
        
#         return service
    
    
    
if __name__=="__main__":
    app.run(debug=True, port=3000)
