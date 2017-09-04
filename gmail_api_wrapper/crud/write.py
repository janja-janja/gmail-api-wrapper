"""Write API for GMAIL."""
from gmail_api_wrapper import USER_ID, UNREAD_LABEL
from gmail_api_wrapper.connection import GmailAPIConnection


class GmailAPIWriteWrapper(object):
    """GMAIL API wrapper."""

    def __init__(self):
        """Init stuff."""
        self.gmail_api = GmailAPIConnection().gmail_api_connect()

    def mark_as_read(self, msg_id):
        """Mark a message as read."""
        body_modifier = {
            'removeLabelIds': [UNREAD_LABEL]
        }
        return self.gmail_api.users().messages().modify(
            userId=USER_ID, id=msg_id, body=body_modifier).execute()

    def bulk_mark_as_read(self, messages=[]):
        """Bulk mark UNREAD emails as READ."""
        for each in messages:
            self.mark_as_read(each['id'])
