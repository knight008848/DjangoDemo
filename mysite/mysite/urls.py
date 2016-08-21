from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.views import hello

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', hello),
    url(r'^hello/$', hello),
    url(r'^platforman/', include('apps.platforman.urls')),
    url(r'^gtaman/', include('apps.gtaman.urls')),
)
