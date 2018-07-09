import logging
from email.mime.text import MIMEText
import base64
from googleapiclient import errors
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from os.path import expanduser, join
import json


module_logger = logging.getLogger('qcbot_log.emails')


def get_addresses():
    """
    Returns:
        dictionary of addresses that includes from str and list of to
    """
    module_logger.info(
        'Getting contact addresses for email.')
    home = join(expanduser('~'), '.google')
    try:
        with open(join(home, 'gmail_contacts.json'), 'r') as fh:
            data = fh.read()
            data = json.loads(data)
            return data
    except IOError:
        module_logger.error(
            'Unable to find required file: {}'.format(
                join(home, 'gmail_contacts.json')))


def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    module_logger.info(
        'Creating email message.')
    message = MIMEText(message_text)
    # print (message.as_string())
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    module_logger.debug(
        'Email msg: {}'.format(message.as_string()))
    return {'raw': base64.urlsafe_b64encode(message.as_string())}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    module_logger.info(
        'Sending email with error report.')
    try:
        message = (service.users().messages().send(
            userId=user_id, body=message).execute())
        module_logger.info(
            'Email sent. Message id: {}.'.format(message['id']))
        return message
    except errors.HttpError as error:
        module_logger.error(
            'Unable to send email. Error: {}'.format(error))


def create_gmail_service():
    """
    Authorizes connection to gmail using stored credentials
    Returns:
        service obj
    """
    module_logger.info(
        'Authorizing gmail use.')
    # scope of authorization
    scopes = 'https://www.googleapis.com/auth/gmail.send'

    # credentials folder
    try:
        home = join(expanduser('~'), '.google')
        store = file.Storage(join(home, 'credentials.json'))
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                join(home, 'client_secret.json'), scopes)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))
        return service
    except IOError:
        module_logger.error(
            'Unable to find required file: {}'.format(
                join(home, 'client_secret.json')))
