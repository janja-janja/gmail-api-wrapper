"""GMAIL Credentials Auth."""
import httplib2
import os

from apiclient import discovery

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


from gmail_api_wrapper import (
    CLIENT_SECRET_FILE_PATH, APPLICATION_NAME, SCOPES,)


class GmailAPIConnection(object):
    """Gmail API connection klass."""

    def _get_connection_flags(self):
        """Get connection flags."""
        try:
            import argparse
            flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()
        except (ImportError,):
            flags = None
        return flags

    def _get_credentials(self):
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
                                       'gmail_api_wrapper.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                CLIENT_SECRET_FILE_PATH, SCOPES)
            flow.user_agent = APPLICATION_NAME
            api_flags = self._get_connection_flags()
            if api_flags:
                credentials = tools.run_flow(flow, store, api_flags)
            else:
                credentials = tools.run(flow, store)
        return credentials

    def gmail_api_connect(self):
        """Get gmail service."""
        creds = self._get_credentials()
        http = creds.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        return service
