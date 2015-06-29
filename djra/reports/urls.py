from django.conf.urls import *

urlpatterns = patterns('djra.reports.views',
    url(r'^$', 'index'),
    url(r'^(?P<report_name>\w+)$', 'report'),
)
