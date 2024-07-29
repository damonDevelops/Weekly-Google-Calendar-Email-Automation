import datetime
import smtplib
import os
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
import pytz

# Define the scope and credentials file
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'path/to/your/credentials.json'

# List of calendar IDs and corresponding labels
CALENDARS = [
    {'id': 'your-calendar-id-1@group.calendar.google.com', 'label': 'Label1'},
    {'id': 'your-calendar-id-2@group.calendar.google.com', 'label': 'Label2'},
    {'id': 'your-calendar-id-3@group.calendar.google.com', 'label': 'Label3'}
]

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_calendar_events(service):
    now = datetime.now(timezone.utc).isoformat()
    week_later = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    events = []

    for calendar in CALENDARS:
        events_result = service.events().list(
            calendarId=calendar['id'],
            timeMin=now,
            timeMax=week_later,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        for event in events_result.get('items', []):
            event['calendarLabel'] = calendar['label']
            events.append(event)

    print("Raw event data:")
    for event in events:
        print(event)

    return events

def format_event_time(event_time, time_zone):
    dt = datetime.fromisoformat(event_time.replace('Z', '+00:00'))
    dt_utc = dt.astimezone(pytz.utc)
    local_tz = pytz.timezone(time_zone)
    local_dt = dt_utc.astimezone(local_tz)
    return local_dt.strftime('%I:%M %p')

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(events):
    message_content = 'Your tasks for the upcoming week:\n\n'
    current_day = None
    
    for event in sorted(events, key=lambda x: datetime.fromisoformat(x['start'].get('dateTime', x['start'].get('date')).replace('Z', '+00:00')).astimezone(pytz.utc)):
        start = event['start'].get('dateTime', event['start'].get('date'))
        time_zone = event.get('start', {}).get('timeZone', 'UTC')
        event_day = datetime.fromisoformat(start.replace('Z', '+00:00')).astimezone(pytz.timezone(time_zone)).strftime('%A')
        event_time = format_event_time(start, time_zone)
        label = event.get('calendarLabel', 'Unknown')
        
        if event_day != current_day:
            if current_day is not None:
                message_content += '\n'
            message_content += f"{event_day}\n"
            current_day = event_day
        
        message_content += f"* {event['summary']} ({label}): {event_time}\n"

    msg = MIMEText(message_content)
    msg['Subject'] = 'Weekly Task Summary'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

def main():
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)
    events = get_calendar_events(service)
    send_email(events)

if __name__ == '__main__':
    main()
