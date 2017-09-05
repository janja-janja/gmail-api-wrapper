"""Read API for GMAIL."""
import json

from dateutil import parser

from gmail_api_wrapper import USER_ID, INBOX_LABEL, UNREAD_LABEL
from gmail_api_wrapper.connection import GmailAPIConnection


class GmailAPIReadWrapper(object):
    """GMAIL API wrapper."""

    def __init__(self):
        """Init stuff."""
        self.gmail_api = GmailAPIConnection().gmail_api_connect()

    def list_messages(self, labels=[]):
        """Retrieve all messages given a label."""
        assert isinstance(labels, (list, tuple,)), (
            '`labels` param must be a list or tuple.')
        all_labels_present = self.get_labels()

        labels = labels if labels else [INBOX_LABEL]

        has_all = all([x in all_labels_present for x in labels])

        assert has_all is True, ('Please provide the correct labels. '
                                 'Available labels are: {}'
                                 .format(','.join(all_labels_present)))

        unread_msgs = self.gmail_api.users().messages().list(
            userId=USER_ID, labelIds=labels).execute()

        try:
            messages = unread_msgs['messages']
        except (KeyError,):
            # No Messages
            messages = []

        return messages

    def get_message(self, msg_id):
        """Get specific message."""
        msg = self.gmail_api.users().messages().get(
            userId=USER_ID, id=msg_id).execute()
        return msg

    def get_unread_messages(self):
        """Get all UNREAD messages."""
        return self.list_messages(labels=[UNREAD_LABEL])

    def serialize_message_headers(self, message_headers):
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
                continue
        return final_payload

    def _get_message_headers(self, message):
        """Get message headers."""
        return message['headers']

    def _get_message_payload(self, message):
        """Get message Payload."""
        return message['payload']

    def _get_message_body(self, message_payload):
        """Get message body."""
        pass

    def check_new_mail(self):
        """Check new messages."""
        final_mails = []
        unread_emails = self.get_unread_messages()
        for each in unread_emails:

            # Get specific message instance
            msg = self.get_message(each['id'])

            # Message Payload
            msg_payload = self._get_message_payload(msg)

            # Message Headers
            msg_headers = self._get_message_headers(msg_payload)

            # Serialize message
            serialized_payload = self.serialize_message_headers(msg_headers)

            final_mails.append(serialized_payload)
        return final_mails

    def get_labels(self):
        """Show basic usage of the Gmail API.

        Creates a Gmail API service object and outputs a list of label
        names of the user's Gmail account.
        """
        results = self.gmail_api.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return [label['name'] for label in labels]

    def get_total_messages(self):
        """Get total messages count."""
        results = self.gmail_api.users().getProfile(userId='me').execute()
        total_messages = {
            'Total Messages': results.get('messagesTotal', None),
            'Total Threads': results.get('threadsTotal', None),
            'Email Address': results.get('emailAddress', None)
        }
        formated_json = json.dumps(total_messages, indent=4)
        return formated_json
