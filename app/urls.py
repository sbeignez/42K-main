from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
    url(r'^$', 'home', name='home'),
    url(r'^runner/login/$', 'runner_login', name='runner_login'),
)
