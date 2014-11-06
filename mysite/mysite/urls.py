from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.views import hello

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    (r'^$', hello),
    (r'^hello/$', hello),
    url(r'^platforman/', include('platforman.urls', namespace="platforman")),
    url(r'^admin/', include(admin.site.urls)),
)
