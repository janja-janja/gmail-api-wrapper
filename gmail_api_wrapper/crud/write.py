"""Gmail API Wrapper Write helper.

Hosts all write operations to the gmail Inbox
"""
import base64

from datetime import date, datetime
from email.mime.text import MIMEText

from dateutil import parser

from gmail_api_wrapper import USER_ID, INBOX_LABEL, UNREAD_LABEL
from gmail_api_wrapper.connection import GmailAPIConnection


class GmailAPIWriteHelper(object):
    """Helper for the write operations."""

    def _get_email_addresses(self, addresses):
        """Get addresses and return them as a list.

        :param: addresses - A CSV string or list of addresses.

        :returns: a list of addresses
        """
        assert isinstance(addresses, (str, list, tuple,)), (
            'Please pass `addresses` as a CSV string, list or tuple.')

        if isinstance(addresses, (list, tuple,)):
            return ','.join(each for each in addresses)

        return addresses

    def _send_mail(self, message):
        """Send an email message.

        :param: message: Message to be sent.
        """
        try:
            sent_msg = self.gmail_api.users().messages().send(
                userId=USER_ID, body=message).execute()
            return sent_msg
        except Exception as err:
            raise Exception('An error occurred: {}'.format(err))

    def _get_epoch_equivalent(self, date_to_format):
        """Get timestamp."""
        epoch = datetime.utcfromtimestamp(0)
        return (date_to_format - epoch).total_seconds() * 1000


class GmailAPIWriteWrapper(GmailAPIWriteHelper):
    """Gmail API write wrapper klass.

    This class hosts write operations to the Gmail mailbox
    """

    def __init__(self):
        """Initialize vital objects."""
        self.gmail_api = GmailAPIConnection().gmail_api_connect()

    def compose_mail(self, subject, body, to, cc=None, bcc=None):
        """Compose new message.

        :param: subject - Email Subject as a string object.

        :param: to - A CSV string or a list of email addresses to
        send the message to

        :param: [cc] - An optional CSV string or a list of email
        addresses to carbon copy the message to

        :param: [bcc] - An optional CSV string or a list of email
        addresses to blind carbon copy the message to
        """
        to_addresses = self._get_email_addresses(to)
        message = MIMEText(body)

        if cc:
            cc_addresses = self._get_email_addresses(cc)
            message['cc'] = cc_addresses

        if bcc:
            bcc_addresses = self._get_email_addresses(bcc)
            message['bcc'] = bcc_addresses

        message['to'] = to_addresses
        message['from'] = USER_ID
        message['subject'] = subject

        b64_raw = base64.urlsafe_b64encode(message.as_bytes())

        message_setting = {
            'snippet': '{}...'.format(body[:10]),
            'raw': b64_raw.decode(),
            'labelIds': [UNREAD_LABEL, INBOX_LABEL]
        }
        sent_msg = self._send_mail(message_setting)
        return sent_msg

    def create_label(self, label_name):
        """Create a new label in your Gmail Mailbox.

        :param: label_name - The name of the label in string format
        """
        assert isinstance(label_name, (str,)), ('Label name must be a string')
        label_settings = {
            'name': label_name
        }
        resp = self.gmail_api.users().labels().create(
            userId=USER_ID, body=label_settings).execute()
        return resp

    def create_signatute(self, signature_body):
        """Create a signature to be associated with your Gmail Mailbox.

        :param: signature_body - The signature in string format
        """
        assert isinstance(signature_body, (str,)), (
            '`signature_body` must be a string')
        pass

    def activate_vacation_responder(self,
                                    body,
                                    date_to_activate,
                                    date_to_deactivate,
                                    restrict_to_contacts=True):
        """Create a vacation responder to your Gmail mailbox.

        :param: body - The actual email responder in string format

        :param: date_to_activate - The date to activate this vacation responder
        . It takes a date, datetime or a string object.

        :param: date_to_deactivate - The date to deactivate this vacation
        responder. It takes a date, datetime or a string object.

        :param: restrict_to_contacts - Bool to allow sending auto-responders
        to people not in your contact list
        """
        assert isinstance(date_to_activate, (str, datetime, date,)), (
            '`date_to_activate` must be a date, datetime or a string object')

        assert isinstance(date_to_deactivate, (str, datetime, date,)), (
            '`date_to_deactivate` must be a date, datetime or a string object')

        if isinstance(date_to_activate, (str,)):
            date_to_activate = parser.parse(date_to_activate)

        if isinstance(date_to_deactivate, (str,)):
            date_to_deactivate = parser.parse(date_to_deactivate)

        assert date_to_activate < date_to_deactivate, (
            'Auto-responder activation date must be grater than {}'.format(
                date_to_deactivate.isoformat()))

        start_time = self._get_epoch_equivalent(date_to_activate)
        end_time = self._get_epoch_equivalent(date_to_deactivate)

        vacation_settings = {
            'enableAutoReply': True,
            'responseBodyHtml': body,
            'restrictToDomain': False,
            'restrictToContacts': restrict_to_contacts,
            'startTime': int(start_time),
            'endTime': int(end_time)
        }

        resp = self.gmail_api.users().settings().updateVacation(
            userId=USER_ID, body=vacation_settings).execute()
        return resp

    def get_vacation_responder(self):
        """Get vacation setting."""
        return self.gmail_api.users().settings().getVacation(
            userId=USER_ID).execute()

    def deactivate_vacation_responder(self, body):
        """Activate your vacation responder."""
        pass
