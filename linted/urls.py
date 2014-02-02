from django.conf.urls import patterns, include, url

from django.contrib import admin
from linted import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'linted.views.index', name='home'),
    url(r'^repository/create', 'linted.views.create_repository', name='create_repository'),
    url(r'^repository/(?P<pk>\d+)/$', views.ViewRepository.as_view(), name='view_repository'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
