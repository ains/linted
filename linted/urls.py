from django.conf.urls import patterns, include, url

from django.contrib import admin
from linted import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'linted.views.index', name='home'),
    url(r'^repository/create', 'linted.views.create_repository', name='create_repository'),
    url(r'^repository/(?P<uuid>[a-zA-Z0-9\-]+)/$', views.view_repoository, name='view_repository'),
    url(r'^repository/(?P<uuid>[a-zA-Z0-9\-]+)/scan$', views.run_scan,name='scan_repository'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
