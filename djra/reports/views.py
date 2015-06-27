from django.template import RequestContext
from django.shortcuts import render_to_response
import datetime
from django.contrib.auth.decorators import login_required
from djra.freeradius.models import Radacct
from .models import build_geo_report

@login_required
def index(request):
    return render_to_response(
        'reports/index.html',
        {'request' : request},
        context_instance = RequestContext(request)
    )

@login_required
def geo_report(request):
    date_range = request.GET.get('drange') or 'today'
    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)
    days = 0
    if date_range == 'today':
        days = 1
        end_date = today +  datetime.timedelta(days=1)
    if date_range == 'yestoday':
        end_date = today
        days = 1
    if date_range == 'last_7':
        end_date = today
        days = 7
    if date_range == 'last_30':
        end_date = today
        days = 30
    begin_date = end_date - datetime.timedelta(days=days)
    sessions = Radacct.objects.filter(acctstarttime__gte=begin_date, acctstarttime__lt=end_date)
        
    #date, city, user_count, sessio_count, session_count
    report = build_geo_report(sessions)

    return render_to_response(
        'reports/geo_report.html',
        {'report' : report, 'request' : request},
        context_instance = RequestContext(request)
    )
