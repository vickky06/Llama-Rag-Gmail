import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
from messages import (
    NO_MESSAGES_FOUND,
    EMAILS_WRITTEN,
    EMAIL_PROCESS_ERROR,
    PROCESSED_EMAIL
)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_text_from_parts(parts):
    text = ''
    if not parts:
        return text
    for part in parts:
        if part['mimeType'] == 'text/plain':
            text += base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        elif 'parts' in part:
            text += get_text_from_parts(part['parts'])
    return text

def get_and_write_emails():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    try:
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])

        if not messages:
            print(NO_MESSAGES_FOUND)
            return

        with open('emails.jsonl', 'w', encoding='utf-8') as f:
            for message in messages:
                email = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                
                headers = email['payload']['headers']
                subject = next(h['value'] for h in headers if h['name'].lower() == 'subject')
                date = next(h['value'] for h in headers if h['name'].lower() == 'date')
                
                raw_content = get_text_from_parts(email['payload'].get('parts', []))
                
                email_object = {
                    'id': message['id'],
                    'subject': subject,
                    'content': raw_content,
                    'date': date
                }
                
                f.write(json.dumps(email_object) + '\n')
                print(f"{PROCESSED_EMAIL} {subject}")

        print(EMAILS_WRITTEN)
    except Exception as error:
        print(f'{EMAIL_PROCESS_ERROR} {error}')

if __name__ == '__main__':
    get_and_write_emails()
