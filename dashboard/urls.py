from django.conf.urls import patterns, url

from dashboard.views import OrdersDashboard, AcceptOrder, CancelOrder, CompleteOrder


urlpatterns = patterns(
    '',
    url(r'^$', OrdersDashboard.as_view(), name="home"),
    url(r'^accept-order/$', AcceptOrder.as_view(), name="accept-order"),
    url(r'^cancel-order/cancel/$', CancelOrder.as_view(), {'cancel_type': 'cancel'}, name="cancel-order-cancel"),
    url(r'^cancel-order/decline/$', CancelOrder.as_view(), {'cancel_type': 'decline'}, name="cancel-order-decline"),
    url(r'^complete-order/$', CompleteOrder.as_view(), name="complete-order"),
)
