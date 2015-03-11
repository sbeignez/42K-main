from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
    url(r'^$', 'home', name='home'),
    url(r'^runner/$', 'runner', name='runner'),
    url(r'^photographer/$', 'photographer', name='photographer'),
    url(r'^tagger/$', 'tagger', name='tagger'),

)
