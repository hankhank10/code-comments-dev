from flask.templating import render_template
from project import secretstuff2
from . import db

from envelopes import Envelope
import secrets


def compose_message(messages, call_to_action_text = None, call_to_action_url = None):

    return render_template(
        '/email-base.html',
        messages = messages, 
        call_to_action_url = call_to_action_url, 
        call_to_action_text = call_to_action_text
    )


def send_message(to_address, subject, body):
    envelope = Envelope(
        from_addr=('admin@codecomments.dev', 'Code Comments'),
        to_addr=(to_address, to_address),
        subject=subject,
        html_body=body
    )
    envelope.send(secretstuff2.mail_smtp_server, login=secretstuff2.mail_username, password=secretstuff2.mail_password, tls=True)


def compose_and_send_message(to_address, subject, messages, call_to_action_text = None, call_to_action_url = None):

    html_body = compose_message(messages, call_to_action_text, call_to_action_url)
    send_message(to_address, subject, html_body)


