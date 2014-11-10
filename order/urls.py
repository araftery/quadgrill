from django.conf.urls import patterns, url

from order.views import OrderHome, SubmitOrder, TrackOrder


urlpatterns = patterns(
    '',
    url(r'^$', OrderHome.as_view(), name="home"),
    url(r'^track/(?P<key>\w+)/$', TrackOrder.as_view(), name="track"),
    url(r'^submit/$', SubmitOrder.as_view(), name="submit"),
)
