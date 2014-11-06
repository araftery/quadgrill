from django import template
from django.core.urlresolvers import resolve

register = template.Library()


# usage: {% navactive request 'comma-separated-list,of-url-pattern-names,to-match'}
@register.simple_tag
def navactive(request, urls):
    urls = [url.strip() for url in urls.split(',')]
    current = resolve(request.path)
    if current.url_name in urls or u'{}:{}'.format(current.namespace, current.url_name) in urls:
        return "active"
    return ''
