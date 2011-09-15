from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djra.views.home', name='home'),
    url(r'^api/0/', include('djra.api.urls')),
    url(r'^radmin/', include('djra.radmin.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url('^account/login/', 'django.contrib.auth.views.login'),
    url('^account/logout/', 'django.contrib.auth.views.logout'),
)
