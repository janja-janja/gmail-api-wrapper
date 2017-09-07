"""Modify API Helper for Gmail APi Wrapper.

Marking Messages as UNREAD or as READ
"""
from gmail_api_wrapper import USER_ID, UNREAD_LABEL, READ_LABEL
from gmail_api_wrapper.connection import GmailAPIConnection


class GmailAPIModifyWrapper(object):
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

    def bulk_mark_as_read(self, message_ids=[]):
        """Bulk mark UNREAD emails as READ.

        TODO: Confirm this
        """
        body_modifier = {
            'addLabelIds': [READ_LABEL],
            'removeLabelIds': [UNREAD_LABEL]
        }
        return self.gmail_api.users().messages().batchModify(
            userId=USER_ID, messageIds=message_ids,
            body=body_modifier
        ).execute()
