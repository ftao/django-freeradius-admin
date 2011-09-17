from django.db import models

from django.db.models import Q
from freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct

class RadUserManager(models.Manager):
    def get_query_set(self):
        return super(RadUserManager, self).get_query_set().filter(attribute='User-Password', op=':=')
            
    def count_info(self):
        total_count = self.values('username').distinct().count()
        suspended_count = (Radcheck.objects
            .filter(attribute='Auth-Type', op=':=', value='Reject')
            .values('username')
            .distinct().count())
    
        return {
            'total' : total_count,
            'suspended' : suspended_count,
            'active' : total_count - suspended_count
        }

    def get_suspended_users(self):
        suspended_users = (Radcheck.objects
            .filter(username__in=usernames, attribute='Auth-Type', op=':=', value='Reject')
            .values_list('username', flat=True)
            .distinct())
        return suspended_users
        
    def query_active_user(self):
        return self.extra(where=['''
            NOT EXISTS(
                SELECT 1 FROM radcheck as rc 
                WHERE rc.username = radcheck.username
                  AND attribute='Auth-Type'
                  AND op=':='
                  AND value='Reject'
            )
            '''])

    def query_suspended_user(self):
        return self.extra(where=['''
            EXISTS(
                SELECT 1 FROM radcheck as rc 
                WHERE rc.username = radcheck.username
                  AND attribute='Auth-Type'
                  AND op=':='
                  AND value='Reject'
            )
            '''])

class RadUser(Radcheck):
    objects = RadUserManager()

    class Meta:
        proxy = True

    @property
    def password(self):
        return self.value

    @property
    def is_suspended(self):
        return Radcheck.objects.filter(
            username=self.username,
            attribute='Auth-Type',
            op=':=',
            value='Reject').exists()
    
    @property
    def groups(self):
        return (Radusergroup.objects
            .filter(username=self.username)
            .order_by('priority')
            .values_list('groupname', flat=True)
            )
        
def get_radgroup_count():
    groups = list(Radusergroup.objects.values_list('groupname', flat=True).distinct())
    groups += list(Radgroupcheck.objects.values_list('groupname', flat=True).distinct())

    return len(set(groups))

