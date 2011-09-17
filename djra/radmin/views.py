from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.conf import settings
from freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct
from djra.api.models import RadUser, get_radgroup_count
from djra.radmin.forms import RadUserFilterForm

def home(request):
    user_count = RadUser.objects.count_info()
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
    query_set = RadUser.objects.all()
    filter_form = RadUserFilterForm(request.GET)
    if filter_form.is_valid():
        is_suspended = filter_form.cleaned_data.get('is_suspended', '')
        if is_suspended == '0':
            query_set = RadUser.objects.query_suspended_user()
        elif is_suspended == '1':
            query_set = RadUser.objects.query_active_user()
            
        q = filter_form.cleaned_data.get('username', '')
        if q:
            query_set = query_set.filter(username__icontains=q)
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

