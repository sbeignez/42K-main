from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from app import views

# ======================= #
# SITE MAP
# ======================= #
# Public links:

# Landing page:
#   / (temp: join BETA)
#   /join/ (1 pager)
# Lists:
#   /races/ (list of countries)
#   /races/hk/ (select years)
#   /races/hk/2015/ (country and year)
# Details:
#   /races/hk/2015/apr/12/marathon-of-hong-kong/ (details)
# Search:
#   /races/search/

# ======================= #
# Private links:

# /home/
# /event/
# /event/add-photos/
# /event/tag-photos/
# /event/add-participants/
# /event/runner/details/
# /event/runner/details/edit/
# /event/photos/
# /event/search/
#
# /user/orders/
# /user/settings/ (preferences)
#
# /site/terms/
# /site/support/
# /site/feedback/

# ======================= #
# Admin links:
# /dashboard/
# /dashboard/tagging-status/


urlpatterns = patterns(
    'app.views',  # prefix

    # ======================= #
    # Public links:
    url(r'^$', 'landing', name='landing'),
    url(r'^join/$', 'join', name='join'),
    url(r'^login/$', 'join', name='join'),  # duplicate
    # Lists:
    # todo:  /races/ (list of countries)
    # todo:  /races/hk/ (select years)
    # todo:  /races/hk/2015/ (country and year)
    # Details:
    # todo:  /races/hk/2015/apr/12/marathon-of-hong-kong/ (details)
    # Search:
    # todo:  /races/search/


    # ======================= #
    # Private links:
    url(r'^home/$', 'RunnerOverview', name='home'),
    url(r'^event/(?P<race_id>[0-9]+)/$', 'event', name='event'),
    url(r'^event/(?P<race_id>[0-9]+)/edit/$', 'event', name='event-edit'),  # todo
    url(r'^event/(?P<race_id>[0-9]+)/follow/$', 'event', name='event-follow'),  # todo
    url(r'^event/photos/add/$', login_required(views.UploadView.as_view()), name='event-photos-add'),
    url(r'^event/photos/tag/', 'tag', name='tag'),
    # todo /event/runner/add/
    # todo /event/runner/details/
    url(r'^event/runner/details/edit/$', 'RunnerInputbib', name='runner-inputbib'),
    url(r'^event/find/$', login_required(views.RunnerView.as_view()), name='event-find'),
    url(r'^event/create/$', 'EventCreate', name='event-create'),
    url(r'^event/photos/$', 'order', name='order'),


    url(r'upload/', views.upload, name='jfu_upload'),  #???
    url(r'^delete/(?P<pk>\d+)$', views.upload_delete, name='jfu_delete'),  #???




    # User pages
    url(r'^user/orders/', login_required(views.OrdersView.as_view()), name='orders'),
    # todo /user/settings/

    # Site links
    url(r'^site/legal/$', 'legal', name='legal'),
    url(r'^site/legal/terms-of-service/$', 'terms', name='terms'),
    url(r'^site/legal/privacy/$', 'privacy', name='privacy'),
    url(r'^site/legal/refunds/$', 'refunds', name='refunds'),
    url(r'^site/terms-of-service/$', 'terms', name='terms'),  # depreciated
    url(r'^site/support/$', 'support', name='support'),
    url(r'^site/feedback/$', 'feedback', name='feedback'),
    # url(r'^site/blog/$', 'blog', name='blog'),
    url(r'^site/media/$', 'media', name='media'),

    # Admins links
    # todo: /dashboard/
    url(r'^dashboard/$', 'dashboard', name='dashboard'),  # todo
    url(r'^dashboard/tagging-status/$', login_required(views.TaggerView.as_view()), name='dash-tag'),
)
