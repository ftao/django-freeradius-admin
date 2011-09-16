from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.conf import settings
from freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct
from djra.api.models import RadUser, get_raduser_count,get_radgroup_count

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
    return render_to_response(
        'radmin/users.html',
        {'query_set' : query_set, 'request' : request},
        context_instance = RequestContext(request)
    )

def groups(request):
    return render_to_response(
        'radmin/groups.html',
        {},
        context_instance = RequestContext(request)
    )

