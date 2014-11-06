from django.conf.urls import patterns, url

from menu.views import MenuHome


urlpatterns = patterns(
    '',
    url(r'^$', MenuHome.as_view(), name="home"),
)
