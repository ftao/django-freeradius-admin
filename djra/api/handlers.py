import re
import string
import random

from piston.handler import BaseHandler
from piston.utils import rc, throttle
from freeradius.models import Radusergroup,Radcheck

DEFAULT_GROUP_NAME = 'default'

def is_raduser_valid(username):
    return not Radcheck.objects.filter(username=username,
                                       attribute='Auth-Type',
                                       op=':=',
                                       value='Reject').exists()

def get_raduser(username):
    record = Radcheck.objects.get(username=username, attribute='User-Password', op=':=')
    groups = Radusergroup.objects.filter(username=username).order_by('priority').values_list('groupname', flat=True)
    return {
        'username' : record.username,
        'password' : record.value,
        'is_valid' : is_raduser_valid(record.username),
        'groups' : groups,
    }

   
def update_raduser(username, password=None, is_valid=None, groups=None):
    #update password 
    record = Radcheck.objects.get(username=username, attribute='User-Password', op=':=')
    if password is not None and record.value != password:
        record.value = password
        record.save()

    #update valid state
    if is_valid is not None:
        if is_valid:
            Radcheck.objects.filter(username=username, attribute='Auth-Type', op=':=', value='Reject').delete()
        else:
            Radcheck.objects.get_or_create(username=username, attribute='Auth-Type', op=':=', value='Reject')
        

    #update groups 
    if groups is not None and type(groups) in (list, tuple):
        old_groups = Radusergroup.objects.filter(username=username).order_by('priority').values_list('groupname', flat=True)
        if set(old_groups) != set(groups):
            to_delete = set(old_groups) - set(groups)
            Radusergroup.objects.filter(username=username, groupname__in=to_delete).delete()

            to_add = set(groups) - set(old_groups)
            for group in to_add:
                Radusergroup.objects.create(username=username, groupname=group)


def gen_random_password(len):
    return ''.join(random.choice(string.digits) for i in xrange(len))

class RadUserHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')

    def read(self, request, username):
        try:
            return get_raduser(username)
        except Radcheck.DoesNotExist:
            return rc.NOT_FOUND
    
    def create(self, request, username=None):
        username = request.POST.get('username', username)
        password = request.POST.get('password', gen_random_password(6))
        groups = request.POST.get('groups', DEFAULT_GROUP_NAME)
        is_valid = request.POST.get('is_valid', '1')
        is_valid = not (is_valid == '0')
        groups = filter(lambda x: len(x) > 0, groups.split(','))

        record, created = Radcheck.objects.get_or_create(username=username, attribute='User-Password',
                                                         op=':=', defaults={'value':password})
 
        if not created:
            return rc.DUPLICATE_ENTRY

        update_raduser(username, password, is_valid, groups)
        return get_raduser(username)

    def update(self, request, username=None):
        username = request.PUT.get('username', username)
        password = request.PUT.get('password', None)
        groups = request.PUT.get('groups', None)
        is_valid = request.PUT.get('is_valid', None)
        if is_valid is not None:
            is_valid = not (is_valid == '0')
        if groups is not None:
            groups = filter(lambda x: len(x) > 0, groups.split(','))

        try:
            update_raduser(username, password, is_valid, groups)
            return get_raduser(username)
        except Radcheck.DoesNotExist:
            return rc.NOT_FOUND
