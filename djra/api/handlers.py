import re

from piston.handler import BaseHandler
from piston.utils import rc, throttle

from freeradius.models import Radusergroup,Radcheck

def is_raduser_valid(username):
    return not Radcheck.objects.filter(username=username,
                                       attribute='Auth-Type',
                                       op=':=',
                                       value='Reject').exists()

def get_raduser(username):
    try:
        record = Radcheck.objects.get(username=username, attribute='User-Password', op=':=')
    except Radcheck.DoesNotExist:
        return None
    return {
        'username' : record.username,
        'password' : record.value,
        'is_valid' : is_raduser_valid(record.username),
    }

   
def update_raduser(username, password=None, is_valid=None):
    try:
        record = Radcheck.objects.get(username=username, attribute='User-Password', op=':=')
    except Radcheck.DoesNotExist:
        return None
    if password is not None and record.value != password:
        record.value = password
        record.save()

    if is_valid is not None:
        if is_valid:
            Radcheck.objects.filter(username=username, attribute='Auth-Type', op=':=', value='Reject').delete()
        else:
            Radcheck.objects.get_or_create(username=username, attribute='Auth-Type', op=':=', value='Reject')
        
    else:
        is_valid = is_raduser_valid(username)
    #TODO group 
    return {'username' : username, 'password' : record.value, 'is_valid' : is_valid}


class RadUserHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')

    def read(self, request, username):
        try:
            record = Radcheck.objects.get(username=username, attribute='User-Password', op=':=')
        except Radcheck.DoesNotExist:
            return rc.NOT_FOUND
        return {
            'username' : record.username,
            'password' : record.value,
            'is_valid' : is_raduser_valid(record.username),
        }

    def create(self, request, username=None):
        username = request.POST.get('username', username)
        password = request.POST.get('password', '')

        record, created = Radcheck.objects.get_or_create(username=username, attribute='User-Password',
                                                        op=':=', defaults={'value':password})
 
        if not created:
            return rc.DUPLICATE_ENTRY

        return {'username' : username, 'password' : password, 'is_valid' : True}

    def update(self, request, username=None):
        username = request.PUT.get('username', username)
        password = request.PUT.get('password', None)
        is_valid = request.POST.get('is_valid', None)
        if is_valid is not None:
            is_valid = not (is_valid == '0')

        raduser =  update_raduser(username, password, is_valid)
        if raduser is None:
            return rc.NOT_FOUND
        else:
            return raduser
    
