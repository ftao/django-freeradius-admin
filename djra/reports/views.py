import datetime
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from .models import build_geo_report, build_user_report, build_server_report

@login_required
def index(request):
    return render_to_response(
        'reports/index.html',
        {'request' : request},
        context_instance = RequestContext(request)
    )

def get_date_range(request):
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

    return begin_date, end_date
 
@login_required
def report(request, report_name):
    pre_defined_dranges = [
        'today',
        'yestoday',
        'last_7',
        'last_30'
    ]
    begin_date, end_date = get_date_range(request)

    template_name = 'reports/%s_report.html' % report_name
    options = {}

    if report_name == 'geo':
        options['threshold'] = (end_date - begin_date).days * 2
        report = build_geo_report(begin_date, end_date, options)
    elif report_name == 'user':
        report = build_user_report(begin_date, end_date, options)
    elif report_name == 'server':
        report = build_server_report(begin_date, end_date, options)
    context = {
        'report' : report, 
        'begin_date' : begin_date,
        'end_date' : end_date,
        'request' : request, 
        'pre_defined_dranges' : pre_defined_dranges
    }
    return render_to_response(
        template_name,
        context,
        context_instance = RequestContext(request)
    )
