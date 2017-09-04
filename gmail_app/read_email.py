"""Read Emails from GMAIL."""
import httplib2
import json
import os

from dateutil import parser

from apiclient import discovery

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'GMAIL API Wrapper'
USER_ID = 'me'
INBOX_LABEL = 'INBOX'
UNREAD_LABEL = 'UNREAD'


class GmailAPI(object):
    """GMAIL API wrapper."""

    def __init__(self):
        """Init stuff."""
        self.flags = self.get_flags()
        self.credentials = self.get_credentials()

    def get_flags(self):
        """Try get flags."""
        try:
            import argparse
            flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()
        except (ImportError,):
            flags = None
        return flags

    def get_credentials(self):
        """Get valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail_app_wrapper.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if self.flags:
                credentials = tools.run_flow(flow, store, self.flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to {}'.format(credential_path))
        return credentials

    def get_service(self):
        """Get gmail service."""
        http = self.credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        return service

    def list_messages(self, label=None):
        """Retrieve all messages given a label."""
        label = label if label else INBOX_LABEL

        service = self.get_service()
        unread_msgs = service.users().messages().list(
            userId=USER_ID, labelIds=[label]).execute()

        try:
            messages = unread_msgs['messages']
        except (KeyError,):
            # No UNREAD MESSAGES
            return []
        # Returns a list of dicts
        return messages

    def get_message(self, msg_id):
        """Get specific message."""
        service = self.get_service()
        msg = service.users().messages().get(
            userId=USER_ID, id=msg_id).execute()

        return msg

    def get_unread_messages(self):
        """Get all UNREAD messages."""
        return self.list_messages(label=UNREAD_LABEL)

    def serialize_message(self, message_headers):
        """Get message payload.

        Get Subject, Date and Sender from the message_headers passed
        """
        final_payload = {}
        for each in message_headers:
            if each['name'] == 'Subject':
                final_payload['subject'] = each['value']

            if each['name'] == 'Date':
                parsed_date = parser.parse(each['value'])
                final_payload['date'] = parsed_date.isoformat()

            if each['name'] == 'From':
                final_payload['from'] = each['value']

            try:
                final_payload['from']
                final_payload['date']
                final_payload['subject']
                break
            except (KeyError,):
                pass
        return final_payload

    def mark_as_read(self, msg_id):
        """Mark a message as read."""
        service = self.get_service()
        body_modifier = {
            'removeLabelIds': [UNREAD_LABEL]
        }
        return service.users().messages().modify(
            userId=USER_ID, id=msg_id, body=body_modifier).execute()

    def bulk_mark_as_read(self, messages=[]):
        """Bulk mark UNREAD emails as READ."""
        messages = messages if messages else self.get_unread_messages()

        for each in messages:
            self.mark_as_read(each['id'])

    def get_message_headers(self, message):
        """Get message headers."""
        return message['headers']

    def get_message_payload(self, message):
        """Get message Payload."""
        return message['payload']

    def check_new_mail(self):
        """Entry Point.

        Checks UNREAD emails
        """
        final_mails = []
        unread_emails = self.get_unread_messages()
        for each in unread_emails:

            # Get specific message instance
            msg = self.get_message(each['id'])

            # Message Payload
            msg_payload = self.get_message_payload(msg)

            # Message Headers
            msg_headers = self.get_message_headers(msg_payload)

            # Serialize message
            serialized_payload = self.serialize_message(msg_headers)

            final_mails.append(serialized_payload)
        return final_mails

    def get_labels(self):
        """Show basic usage of the Gmail API.

        Creates a Gmail API service object and outputs a list of label
        names of the user's Gmail account.
        """
        service = self.get_service()
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        print("LABEL TYPE\t\t\tLABEL NAME\n")
        for idx, label in enumerate(labels):
            print("{}. {}\t\t\t{}".format(
                  idx + 1, label['type'], label['name']))
        print("\n")
        return True

    def get_total_messages(self):
        """Get total messages count."""
        service = self.get_service()
        results = service.users().getProfile(userId='me').execute()
        total_messages = {
            'Total Messages': results.get('messagesTotal', None),
            'Total Threads': results.get('threadsTotal', None),
            'Email Address': results.get('emailAddress', None)
        }
        formated_json = json.dumps(total_messages, indent=4)
        return formated_json


if __name__ == '__main__':
    api = GmailAPI()
    mails = api.check_new_mail()
    print(mails)
