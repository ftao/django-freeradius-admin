from django.db import models

from django.db.models import Q
from freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct

class RadUser(Radcheck):

    class Meta:
        proxy = True

    @property
    def password(self):
        assert self.attribute == 'User-Password'
        assert self.op == ':='
        return self.value

    @property
    def is_suspended(self):
        assert self.attribute == 'User-Password'
        assert self.op == ':='
        return Radcheck.objects.filter(
            username=self.username,
            attribute='Auth-Type',
            op=':=',
            value='Reject').exists()
    
def get_raduser_count():
    total_count = Radcheck.objects.filter(attribute='User-Password', op=':=')\
                                  .values('username')\
                                  .distinct().count()
    suspended_count = Radcheck.objects.filter(attribute='Auth-Type',
                                              op=':=',
                                              value='Reject')\
                                      .values('username')\
                                      .distinct().count()
 
    return {
        'total' : total_count,
        'suspended' : suspended_count,
        'active' : total_count - suspended_count
    }


def get_radgroup_count():
    groups = list(Radusergroup.objects.values_list('groupname', flat=True).distinct())
    groups += list(Radgroupcheck.objects.values_list('groupname', flat=True).distinct())

    return len(set(groups))

