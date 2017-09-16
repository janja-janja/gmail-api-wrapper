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
        self.all_labels_present = self.get_labels()

    def list_messages(self, labels=[], sender=None):
        """Retrieve all messages given a label.

        :param: [labels:list] - A list of the various labels you wish to target
        e.g INBOX, SPAM, UNREAD e.t.c

        :param: [sender:string] - CSV with email addresses to allow targetting
        messages from specific email addresses
        """
        sender = 'from:{}'.format(sender) if sender else 'from:'

        assert isinstance(labels, (list, tuple,)), (
            '`labels` param must be a list or tuple.')

        labels = labels if labels else [INBOX_LABEL]

        has_all = all([x in self.all_labels_present for x in labels])

        assert has_all is True, ('Please provide the correct labels. '
                                 'Available labels are: {}'
                                 .format(','.join(self.all_labels_present)))

        messages_list = self.gmail_api.users().messages().list(
            userId=USER_ID, labelIds=labels, q=sender).execute()

        messages = messages_list.get('messages', [])
        return messages

    def get_message(self, msg_id):
        """Get specific message.

        :param: msg_id - Message ID. A Google object id
        """
        msg = self.gmail_api.users().messages().get(
            userId=USER_ID, id=msg_id).execute()
        return msg

    def get_unread_messages(self, sender=None):
        """Get all UNREAD messages.

        :param: [sender:string] - CSV with email addresses to allow targetting
        messages from specific email addresses
        """
        return self.list_messages(labels=[UNREAD_LABEL], sender=sender)

    def serialize_message_headers(self, message_headers):
        """Get message payload.

        Get Subject, Date and Sender from the message_headers passed

        :param: message_headers - Headers associated with a particular message
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
        """Get message headers.

        :param: message - Gmail message object
        """
        return message['headers']

    def _get_message_payload(self, message):
        """Get message Payload.

        :param: message - Gmail message object
        """
        return message['payload']

    def _get_message_body(self, message_payload):
        """Get message body.

        :param: message_payload - Gmail message payload object

        Returns a base64 encoded string. You can further decode it to get
        the actual message.
        base64.b64decode(message_payload['parts'][0]['body']['data'])
        """
        try:
            return message_payload['parts'][0]['body']['data']
        except (KeyError,):
            return []

    def check_new_mail(self, sender=None):
        """Check new messages.

        :param: sender:string - CSV with email addresses to allow targetting
        messages from specific email addresses
        """
        final_mails = []
        unread_emails = self.get_unread_messages(sender=sender)
        for each in unread_emails:

            # Get specific message instance
            msg = self.get_message(each['id'])

            # Message Payload
            msg_payload = self._get_message_payload(msg)

            # Message Headers
            msg_headers = self._get_message_headers(msg_payload)

            # Serialize message
            serialized_payload = self.serialize_message_headers(msg_headers)

            # Get message body
            serialized_payload['base64_msg_body'] = self._get_message_body(
                msg_payload)

            final_mails.append(serialized_payload)
        return final_mails

    def get_labels(self):
        """Show basic usage of the Gmail API.

        Creates a Gmail API service object and outputs a list of label
        names of the user's Gmail account.
        """
        results = self.gmail_api.users().labels().list(
            userId=USER_ID).execute()
        labels = results.get('labels', [])
        return [label['name'] for label in labels]

    def get_total_messages(self):
        """Get total messages count."""
        results = self.gmail_api.users().getProfile(userId=USER_ID).execute()
        total_messages = {
            'Total Messages': results.get('messagesTotal', 0),
            'Total Threads': results.get('threadsTotal', 0),
            'Email Address': results.get('emailAddress', USER_ID)
        }
        formated_json = json.dumps(total_messages, indent=4)
        return formated_json
