"""Modify API Helper for Gmail APi Wrapper.

Marking Messages as UNREAD or as READ
"""
from gmail_api_wrapper import READ_LABEL, UNREAD_LABEL, USER_ID
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
        resp = self.gmail_api.users().messages().modify(
            userId=USER_ID, id=msg_id, body=body_modifier).execute()
        return resp

    def bulk_mark_as_read(self, message_ids=[]):
        """Bulk mark UNREAD emails as READ.

        TODO: Confirm this
        """
        body_modifier = {
            'messageIds': message_ids,
            'addLabelIds': [READ_LABEL],
            'removeLabelIds': [UNREAD_LABEL]
        }
        resp = self.gmail_api.users().messages().batchModify(
            userId=USER_ID, body=body_modifier).execute()
        return resp
