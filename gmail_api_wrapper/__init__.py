"""Gmail API Wrapper."""
import os


CLIENT_SECRET_FILE_PATH = os.getenv('GAW_CLIENT_SECRET_FILE_PATH'), (
    'Add path to the `client_secret.json` using GAW_CLIENT_SECRET_FILE_PATH '
    'env variable')
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/client_secret.json
SCOPES = os.getenv('GAW_SCOPES', [])

APPLICATION_NAME = os.getenv('GAW_APPLICATION_NAME', 'GMAIL API Wrapper')
USER_ID = os.getenv('GAW_USER_ID', 'me')

INBOX_LABEL = 'INBOX'
UNREAD_LABEL = 'UNREAD'
READ_LABEL = 'READ'
