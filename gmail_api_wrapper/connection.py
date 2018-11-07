"""GMAIL Credentials Auth."""
import os
import sys

from apiclient import discovery

from gmail_api_wrapper import APPLICATION_NAME

import httplib2


from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleAPIConnection(object):
    """An API connection establisher for Google APIs."""

    def __init__(self, service, version):
        """Google API connection establisher.

        :param: service - Service to establish a connection to e.g gmail
        """
        self.service = service
        self.version = version

        # If modifying these scopes, delete your previously saved credentials
        # at ~/.credentials/gmail-api-wrapper-py.json.json
        self.scopes = os.environ['GAW_SCOPES']

        self.ca_certs = os.getenv('GAW_CA_CERTS_PEM_FILE')
        self.disable_ssl = self._get_bool_value(
            os.getenv('GAW_DISABLE_SSL_CERTS', False))

    def _get_bool_value(self, value):
        """Return bool value from string."""
        bool_list = ['True', 'true', 'Yes', 'yes']
        return True if value in bool_list else False

    def _get_connection_flags(self):
        """Get connection flags."""
        try:
            import argparse
            flags = argparse.ArgumentParser(
                parents=[tools.argparser]).parse_args()
        except (ImportError,):
            flags = None
        return flags

    def _get_client_secret_filename(self, file_path):
        """Get the client secret filename given the filepath.

        :param: file_path - Path to the client secret file
        """
        nix = ['darwin', 'linux{}'.format(x for x in range(100))]

        if sys.platform in nix:
            parts = file_path.split('/')
        else:
            # Windows
            parts = []
        size = len(parts)
        return parts[size - 1]

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
            credential_dir, 'client_secret.json')

        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(credential_path, self.scopes)
            flow.user_agent = APPLICATION_NAME
            api_flags = self._get_connection_flags()
            if api_flags:
                credentials = tools.run_flow(flow, store, api_flags)
            else:
                credentials = tools.run(flow, store)
        return credentials

    def get_service(self):
        """Establish Google service."""
        creds = self._get_credentials()
        request = httplib2.Http(
            ca_certs=self.ca_certs,
            disable_ssl_certificate_validation=self.disable_ssl)
        http = creds.authorize(request)
        service = discovery.build(self.service, self.version, http=http)
        return service


class GmailAPIConnection(object):
    """Gmail API connection klass."""

    def gmail_api_connect(self):
        """Get gmail service.

        Get authenticated to the Gmail API.
        """
        google_api = GoogleAPIConnection(service='gmail', version='v1')
        service = google_api.get_service()
        return service
