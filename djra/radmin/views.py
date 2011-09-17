from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.conf import settings
from freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct
from djra.api.models import RadUser, get_raduser_count,get_radgroup_count
from djra.radmin.forms import RadUserFilterForm

def home(request):
    user_count = get_raduser_count()
    group_count = get_radgroup_count()
    return render_to_response(
        'radmin/home.html',
        {'active_user_count' : user_count['active'],
         'suspended_user_count' : user_count['suspended'],
         'group_count' : group_count,
        },
        context_instance = RequestContext(request)
    )

def users(request):
    query_set = RadUser.objects.filter(attribute='User-Password', op=':=')
    filter_form = RadUserFilterForm(request.GET)
    filter_form.is_valid()
    q = filter_form.cleaned_data.get('username', '')
    if q:
        query_set = query_set.filter(username__icontains=q)
    is_suspended = filter_form.cleaned_data.get('is_suspended', '-1')
    if is_suspended in ('0', '1'):
        suspended_users = Radcheck.objects\
            .filter(attribute='Auth-Type', op=':=', value='Reject')\
            .values_list('username', flat=True)\
            .distinct()
        if is_suspended == '0':
            query_set = query_set.exclude(username__in=suspended_users)
        else:
            query_set = query_set.filter(username__in=suspended_users)
    return render_to_response(
        'radmin/users.html',
        {'query_set' : query_set, 'filter_form' : filter_form, 'request' : request},
        context_instance = RequestContext(request)
    )

def groups(request):
    return render_to_response(
        'radmin/groups.html',
        {},
        context_instance = RequestContext(request)
    )

