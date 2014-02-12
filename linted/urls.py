from django.conf.urls import patterns, include, url

from django.contrib import admin
from linted import views

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', 'linted.views.index', name='home'),
                       url(r'^repository/$', views.repository_list, name='repository_list'),
                       url(r'^repository/create/$', views.create_repository, name='create_repository'),
                       url(r'^repository/(?P<uuid>[a-zA-Z0-9\-]+)/$', views.view_repoository, name='view_repository'),
                       url(r'^repository/(?P<uuid>[a-zA-Z0-9\-]+)/scan$', views.run_scan, name='scan_repository'),
                       url(r'^repository/(?P<uuid>[a-zA-Z0-9\-]+)/scanner$', views.scanner_settings,
                           name='scanner_settings'),

                       url(r'^admin/', include(admin.site.urls)),
)