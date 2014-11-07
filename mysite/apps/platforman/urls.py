from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='platform_list'),
    url(r'^(?P<object_id>\d+)/$', views.detail, name='platform_detail'),
)
