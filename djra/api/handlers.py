import re
import string
import random

from django.db.models import Q

from piston.handler import BaseHandler
from piston.utils import rc, throttle
from piston.utils import validate, FormValidationError

from freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct
from djra.api.forms import RadUserForm
from djra.api.models import RadUser

DEFAULT_GROUP_NAME = 'default'

def gen_random_password(len):
    return ''.join(random.choice(string.digits) for i in xrange(len))

class RadUserHandler(BaseHandler):
    model = RadUser
    fields = ('username', 'password', 'is_suspended', 'groups')
    allowed_methods = ('GET', 'POST', 'PUT')

    def read(self, request, username=None):
        if username is None:
            query_set = RadUser.objects.all()
            is_suspended = request.GET.get('is_suspended', None)
            if is_suspended == '0':
                query_set = RadUser.objects.query_suspended_user()
            elif is_suspended == '1':
                query_set = RadUser.objects.query_active_user()
                    
            q = request.GET.get('q', '')
            if q:
                query_set = query_set.filter(username__icontains=q)
        
            usernames = query_set.values_list('username', flat=True).distinct()
            return usernames
        else:
            try:
                return RadUser.objects.get(username=username)
            except RadUser.DoesNotExist:
                return rc.NOT_FOUND
        
    def create(self, request, username=None):
        #do somethins simliar to validate decorator ,
        #but we fill in some default values
        raw_data = {
            'username' : username,
            'password' : gen_random_password(6),
            'groups' : DEFAULT_GROUP_NAME,
            'is_suspended' : '0'
        }
        raw_data.update(request.POST.items())
        form = RadUserForm(raw_data)

        if not form.is_valid():
            raise FormValidationError(form)

        data = form.cleaned_data
        username = data['username']
        password = data['password']
        groups = data['groups'].split(',')
        is_suspended = data['is_suspended']

        record, created = RadUser.objects.get_or_create(username=username, defaults={'value':password})
 
        if not created:
            return rc.DUPLICATE_ENTRY

        record.update(password, is_suspended, groups)
        return RadUser.objects.get(username=username)

    def update(self, request, username=None):
        raw_data = {
            'username' : username,
        }
        raw_data.update(request.PUT.items())

        form = RadUserForm(raw_data)
        if not form.is_valid():
            raise FormValidationError(form)

        data = form.cleaned_data

        username = data['username']
        password = data['password'] if 'password' in raw_data else None
        groups = data['groups'].split(',') if 'groups' in raw_data else None
        is_suspended = data['is_suspended'] if 'is_suspended' in raw_data else None

        try:
            raduser = RadUser.objects.get(username=username)
            raduser.update(password, is_suspended, groups)
            return raduser
        except Radcheck.DoesNotExist:
            return rc.NOT_FOUND


class RadGroupHandler(BaseHandler):
    allowed_methods = ('GET',)# 'POST', 'PUT')

    def read(self, request, groupname=None):
        if groupname is None:
            groups_1 =  Radgroupcheck.objects.values_list('groupname', flat=True).distinct()
            groups_2 =  Radusergroup.objects.values_list('groupname', flat=True).distinct()
            groups = list(set(groups_1).union(set(groups_2)))
            return groups
            
        else:
            radgc_records =  Radgroupcheck.objects.filter(groupname=groupname)
            user_count =  Radusergroup.objects.filter(groupname=groupname).distinct().count()

            if len(radgc_records) == 0 and user_count == 0:
                return rc.NOT_FOUND

            attrs = [] 
            for radgc in radgc_records:
                attrs.append({'attribute' : radgc.attribute,
                              'op' : radgc.op,
                              'value' : radgc.value})
            return {'groupname' : groupname, 'attrs' : attrs, 'user_count' : user_count}
    
class RadAcctHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Radacct
    exclude = ('id', 'groupname', 'realm', 'connectinfo_start', 'connectinfo_stop',
               'calledstationid', 'acctstartdelay', 'acctstopdelay', 'xascendsessionsvrkey')

    def read(self, request, username=None):
        records = Radacct.objects.filter(username=username)
        if request.GET.get('type', None) == 'connected':
            records = records.filter(acctstoptime=None)
        limit = request.GET.get('limit', '')
        try:
            limit = int(limit)
            if limit > 100:
                limit = 100
            if limit <= 0:
                raise ValueError("limit must be postive")
        except ValueError:
            limit = 20
        records = records.order_by('-acctstarttime')[:limit]

        return records
