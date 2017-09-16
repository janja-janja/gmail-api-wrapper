"""GMAIL Credentials Auth."""
import httplib2
import os

from apiclient import discovery

from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


from gmail_api_wrapper import APPLICATION_NAME


class GmailAPIConnection(object):
    """Gmail API connection klass."""

    def __init__(self):
        """Init."""
        self.client_secret_file_name = 'client_secret.json'
        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/client_secret.json
        self.scopes = os.environ['GAW_SCOPES']
        self.ca_certs = os.getenv('GWA_CA_CERTS_PEM_FILE')

        assert os.path.exists('~/.credentials/{}'.format(
            self.client_secret_file_name)) is True, (
            'Ensure you have saved client_secret.json file in ~/.credentials '
            'folder')

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
        credential_path = os.path.join(
            credential_dir, self.client_secret_file_name)

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                self.client_secret_file_name, self.scopes)
            flow.user_agent = APPLICATION_NAME
            api_flags = self._get_connection_flags()
            if api_flags:
                credentials = tools.run_flow(flow, store, api_flags)
            else:
                credentials = tools.run(flow, store)
        return credentials

    def gmail_api_connect(self):
        """Get gmail service.

        Get authenticated to the Gmail API.
        """
        creds = self._get_credentials()
        request = httplib2.Http(ca_certs=self.ca_certs)
        http = creds.authorize(request)
        service = discovery.build('gmail', 'v1', http=http)
        return service
