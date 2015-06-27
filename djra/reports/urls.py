from django.conf.urls import *

urlpatterns = patterns('djra.reports.views',
    url(r'^$', 'index'),
    url(r'^geo$', 'geo_report'),
)
