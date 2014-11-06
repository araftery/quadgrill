from django.conf.urls import patterns, url

from order.views import OrderHome, SubmitOrder


urlpatterns = patterns(
    '',
    url(r'^$', OrderHome.as_view(), name="home"),
    url(r'^submit/$', SubmitOrder.as_view(), name="submit"),
)
