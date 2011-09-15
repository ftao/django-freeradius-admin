from django.conf.urls.defaults import *

urlpatterns = patterns('djra.radmin.views',
    url(r'^$', 'home'), 
    url(r'^users/$', 'users'), 
    url(r'^groups/$', 'groups'), 
)
