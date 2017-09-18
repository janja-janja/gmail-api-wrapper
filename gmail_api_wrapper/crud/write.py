"""Gmail API Wrapper Write helper.

Hosts all write operations to the gmail Inbox
"""
from datetime import date, datetime

from dateutil import parser

from gmail_api_wrapper import USER_ID
from gmail_api_wrapper.connection import GmailAPIConnection


class GmailAPIWriteWrapper(object):
    """Gmail API write wrapper klass."""

    def __init__(self):
        """Initialize vital objects."""
        self.gmail_api = GmailAPIConnection().gmail_api_connect()

    def _get_email_addresses(self, addresses):
        """Get addresses and return them as a list.

        :param: addresses - A CSV string or list of addresses.

        :returns: a list of addresses
        """
        assert isinstance(addresses, (str, list, tuple,)), (
            'Please pass `addresses` as a CSV string, list or tuple.')

        if isinstance(addresses, (list, tuple,)):
            return addresses

        return addresses.split(',')

    def compose_mail(self,
                     subject,
                     body,
                     to_addresses,
                     cc_addresses=None,
                     bcc_addresses=None):
        """Compose new message.

        :param: subject - Email Subject as a string object.

        :param: to_addresses - A CSV string or a list of email addresses to
        send the message to

        :param: [cc_addresses] - An optional CSV string or a list of email
        addresses to carbon copy the message to

        :param: [bcc_addresses] - An optional CSV string or a list of email
        addresses to blind carbon copy the message to
        """
        to_addresses = self._get_email_addresses(to_addresses)

        if cc_addresses:
            cc_addresses = self._get_email_addresses(cc_addresses)

        if bcc_addresses:
            bcc_addresses = self._get_email_addresses(bcc_addresses)

        pass

    def create_label(self, label_name):
        """Create a new label in your Gmail Mailbox.

        :param: label_name - The name of the label in string format
        """
        assert isinstance(label_name, (str,)), ('Label name must be a string')
        pass

    def create_signatute(self, signature_body):
        """Create a signature to be associated with your Gmail Mailbox.

        :param: signature_body - The signature in string format
        """
        assert isinstance(signature_body, (str,)), (
            '`signature_body` must be a string')
        pass

    def _get_epoch_equivalent(self, date_to_format):
        """Get timestamp."""
        epoch = datetime.utcfromtimestamp(0)
        return (date_to_format - epoch).total_seconds() * 1000

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
                date_to_activate.isoformat()))

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
