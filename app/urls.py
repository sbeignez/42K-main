from django.conf.urls import patterns, url

from app import views

urlpatterns = patterns('app.views',
    url(r'^$', 'home', name='home'),
    url(r'^runner/$', 'runner', name='runner'),
    url(r'^photographer/$', 'photographer', name='photographer'),
    url(r'^tagger/$', views.TaggerView.as_view(), name='tagger'),


)
