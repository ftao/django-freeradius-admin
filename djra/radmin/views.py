from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.conf import settings

def home(request):
    return render_to_response(
        'radmin/home.html',
        {},
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

