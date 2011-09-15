from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.conf import settings
from djra.api.models import get_raduser_count,get_radgroup_count

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
    return render_to_response(
        'radmin/users.html',
        {},
        context_instance = RequestContext(request)
    )

def groups(request):
    return render_to_response(
        'radmin/groups.html',
        {},
        context_instance = RequestContext(request)
    )

