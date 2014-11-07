from django.conf.urls import patterns, url

from dashboard.views import OrdersDashboard, AcceptOrder


urlpatterns = patterns(
    '',
    url(r'^$', OrdersDashboard.as_view(), name="home"),
    url(r'^accept-order/$', AcceptOrder.as_view(), name="accept-order")
)
