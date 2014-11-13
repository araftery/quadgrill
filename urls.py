from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView


urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(pattern_name='menu:home')),
    url(r'^menu/', include('menu.urls', namespace='menu', app_name='menu')),
    url(r'^order/', include('order.urls', namespace='order', app_name='order')),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard', app_name='dashboard')),
    url(r'^admin/', include(admin.site.urls)),
)
