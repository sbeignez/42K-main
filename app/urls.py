from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = patterns('app.views',
    url(r'^$', 'home', name='home'),
    url(r'^runner/$', views.RunnerView.as_view(), name='runner'),
    url(r'^photographer/$', views.UploadView.as_view(), name='photographer'),
    url(r'^tagger/$', views.TaggerView.as_view(), name='tagger'),
    url(r'^order/$', 'order', name='order'),
    url(r'^orders/', login_required(views.OrdersView.as_view()), name='orders'),
    url( r'upload/', views.upload, name = 'jfu_upload' ),
    url( r'^delete/(?P<pk>\d+)$', views.upload_delete, name = 'jfu_delete' ),
)
