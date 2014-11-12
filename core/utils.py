import json
import requests

from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse

from core.tasks import send_text as send_text_task


def send_text(template_name, recipient, context):
    send_text_task(template_name, recipient, context)


def shorten_url(pattern, **kwargs):
    url = u'http://{}{}'.format(get_current_site(None).domain, reverse('order:track', kwargs=kwargs))
    data = {'longUrl': url}
    print data
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post('https://www.googleapis.com/urlshortener/v1/url', data=json.dumps(data), headers=headers)
    result = r.json()
    return result.get('id')
