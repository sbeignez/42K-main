from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns(
    '',

    # Site: allauth
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),

    # Site: Admin
    url(r'^admin/', include(admin.site.urls)),

    # Site: Payments
    url('^payments/', include('payments.urls')),

    url(r'', include('app.urls')),
)