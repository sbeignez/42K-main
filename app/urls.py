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
    # todo: /event/
    url(r'^event/add-photos/$', login_required(views.UploadView.as_view()), name='photographer'),
    url(r'^event/tag-photos/', 'tag', name='tag'),
    # todo /event/add-participants/
    # todo /event/runner/details/
    url(r'^event/runner/details/edit/$', 'RunnerInputbib', name='runner-inputbib'),
    url(r'^event/search-event/$', login_required(views.RunnerView.as_view()), name='runner'),
    url(r'^event/create-event/$', 'add_race', name='add_race'),
    url(r'^event/photos/$', 'order', name='order'),


    url(r'upload/', views.upload, name='jfu_upload'),  #???
    url(r'^delete/(?P<pk>\d+)$', views.upload_delete, name='jfu_delete'),  #???




    # User pages
    url(r'^user/orders/', login_required(views.OrdersView.as_view()), name='orders'),
    # todo /user/settings/

    # Site links
    url(r'^site/terms-of-service/$', 'terms', name='terms'),
    url(r'^site/support/$', 'support', name='support'),
    url(r'^site/feedback/$', 'feedback', name='feedback'),

    # Admins links
    # todo: /dashboard/
    url(r'^dashboard/$', 'dashboard', name='dashboard'),  # todo
    url(r'^dashboard/tagging-status/$', login_required(views.TaggerView.as_view()), name='dash-tag'),
)
