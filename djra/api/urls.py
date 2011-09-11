from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from djra.api.handlers import RadUserHandler,RadGroupHandler

#auth = HttpBasicAuthentication(realm="My Realm")
#ad = { 'authentication': auth }

raduser_resource = Resource(handler=RadUserHandler)#, **ad)
radgroup_resource = Resource(handler=RadGroupHandler)#, **ad)
#arbitrary_resource = Resource(handler=ArbitraryDataHandler, **ad)

urlpatterns = patterns('',
    url(r'^radusers/$', raduser_resource), 
    url(r'^radusers/(?P<username>[^/]+)/$', raduser_resource), 

    url(r'^radgroups/$', radgroup_resource), 
    url(r'^radgroups/(?P<groupname>[^/]+)/$', radgroup_resource), 
    #url(r'^other/(?P<username>[^/]+)/(?P<data>.+)/$', arbitrary_resource), 
)
