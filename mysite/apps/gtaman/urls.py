from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^(?P<object_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<object_id>\d+)/download/$', views.download_id, name='detail_id'),
    url(r'^download/(?P<ponumber>\w+)/$', views.download_po, name='download_po'),
)
