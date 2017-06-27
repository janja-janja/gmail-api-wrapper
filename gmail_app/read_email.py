"""Read Emails from GMAIL."""
import httplib2
import json
import os

from apiclient import discovery

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


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
                                       'gmail_app_email_reader.json')

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

    def get_label(self):
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
    api.get_label()
    total_messages = api.get_total_messages()
    print(total_messages)
