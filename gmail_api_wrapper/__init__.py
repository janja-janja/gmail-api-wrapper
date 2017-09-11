"""Gmail API Wrapper."""
import os


APPLICATION_NAME = os.getenv('GAW_APPLICATION_NAME', 'GMAIL API Wrapper')
USER_ID = os.getenv('GAW_USER_ID', 'me')

INBOX_LABEL = 'INBOX'
UNREAD_LABEL = 'UNREAD'
READ_LABEL = 'READ'
