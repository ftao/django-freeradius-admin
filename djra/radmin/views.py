from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.conf import settings
from django.contrib import messages

from freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct
from djra.api.models import RadUser, get_groups, get_radgroup_count
from djra.radmin.forms import RadUserFilterForm,RadUserForm,NewRadUserForm


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

def user_detail(request, username):
    try:
        raduser = RadUser.objects.get(username=username)
    except RadUser.DoesNotExist:
        return HttpResponseNotFound('not found')
    if request.method == 'POST':
        form = RadUserForm(request.POST)
        if form.is_valid():
            assert raduser.username == form.cleaned_data['username']
            raduser.update(password=form.cleaned_data['password'],
                           is_suspended=form.cleaned_data['is_suspended'],
                           groups=form.cleaned_data['groups'].split(','))
            messages.success(request, 'User %s saved.' %raduser.username)
    else:
        data = {
            u'username' : raduser.username,
            u'password' : raduser.password,
            u'is_suspended' : raduser.is_suspended, 
            u'groups' : u','.join(raduser.groups),
        }
        form = RadUserForm(data)
    return render_to_response(
        'radmin/user_detail.html',
        {'raduser' : raduser, 'form' : form, 'request' : request},
        context_instance = RequestContext(request)
    )

def user_sessions(request, username):

    try:
        raduser = RadUser.objects.get(username=username)
    except RadUser.DoesNotExist:
        return HttpResponseNotFound('not found')
    sessions =  Radacct.objects.filter(username=username).order_by('-acctstarttime')
    return render_to_response(
        'radmin/user_sessions.html',
        {'raduser' : raduser, 'sessions' : sessions, 'request' : request},
        context_instance = RequestContext(request)
    )


def create_user(request):
    if request.method == 'POST':
        form = NewRadUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            raduser, created = RadUser.objects.get_or_create(username=username,
                                                             defaults={'value' : form.cleaned_data['password']})
            if not created:
                messages.error(request, 'User %s already exists.' %username)
            else:    
                raduser.update(password=form.cleaned_data['password'],
                            is_suspended=form.cleaned_data['is_suspended'],
                            groups=form.cleaned_data['groups'].split(','))
                messages.success(request, 'User %s created.' %username)
                return HttpResponseRedirect(reverse('djra.radmin.views.user_detail', kwargs={'username' : username}))
    else:
        form = NewRadUserForm()
        
    return render_to_response(
        'radmin/create_user.html',
        {'form' : form, 'request' : request},
        context_instance = RequestContext(request)
    )

def groups(request):
    groups = get_groups()
    return render_to_response(
        'radmin/groups.html',
        {'groups' : groups, 'request' : request},
        context_instance = RequestContext(request)
    )
