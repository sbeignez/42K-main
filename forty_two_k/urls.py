from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forty_two_k.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
     {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url('^payments/', include('payments.urls')),
    url(r'', include('app.urls')),
)
