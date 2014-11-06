from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quadgrill.views.home', name='home'),
    url(r'^menu/', include('menu.urls', namespace='menu', app_name='menu')),
    url(r'^order/', include('order.urls', namespace='order', app_name='order')),
    url(r'^admin/', include(admin.site.urls)),
)
