import logging
import textwrap

from django.conf import settings
from django.template.loader import get_template
from django.template import Context

from celery.task import task
from twilio.rest import TwilioRestClient


logger = logging.getLogger(__name__)


@task
def send_text(template_name, recipient, context):
    logger.info('Sending {} text to {}'.format(template_name, recipient))
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = TwilioRestClient(account_sid, auth_token)
    plaintext = get_template(u'texts/{}.txt'.format(template_name))
    d = Context(context)
    body = plaintext.render(d)
    bodies = textwrap.wrap(body, 160)
    for body in bodies:
        message = client.sms.messages.create(
            body=body,
            to=recipient,
            from_=settings.TWILIO_PHONE_NUMBER,
        )
