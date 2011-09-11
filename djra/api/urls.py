from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication

from djra.api.handlers import RadUserHandler,RadGroupHandler,RadAcctHandler

#auth = HttpBasicAuthentication(realm="My Realm")
#ad = { 'authentication': auth }

raduser_resource = Resource(handler=RadUserHandler)#, **ad)
radgroup_resource = Resource(handler=RadGroupHandler)#, **ad)
radacct_resource = Resource(handler=RadAcctHandler)#, **ad)

urlpatterns = patterns('',
    url(r'^radusers/$', raduser_resource), 
    url(r'^radusers/(?P<username>[^/]+)/$', raduser_resource), 

    url(r'^radgroups/$', radgroup_resource), 
    url(r'^radgroups/(?P<groupname>[^/]+)/$', radgroup_resource), 
    #url(r'^other/(?P<username>[^/]+)/(?P<data>.+)/$', arbitrary_resource), 
    url(r'^radusers/(?P<username>[^/]+)/acct/$', radacct_resource), 
)
