from django.conf.urls.defaults import *

urlpatterns = patterns('djra.radmin.views',
    url(r'^$', 'home'), 
    url(r'^users/$', 'users'), 
    url(r'^users/create/$', 'create_user'), 
    url(r'^user/(?P<username>[\w\.@\-]+)/$', 'user_detail'), 
    url(r'^groups/$', 'groups'), 
)
