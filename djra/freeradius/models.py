from django.db import models
from .raw_models import *

class RadUserQuerySet(models.query.QuerySet):
    '''Use this class to define methods on queryset itself.'''


    def filter(self, *args, **kwargs):
        is_online = None
        is_active = None
        for k,v in kwargs.items():
            if k == 'is_online' or k.startswith('is_online__'):
                is_online = v
                del kwargs[k]
            elif k == 'is_active' or k.startswith('is_active__'):
                is_active = v
                del kwargs[k]

        q = super(RadUserQuerySet, self).filter(*args, **kwargs)
        if is_online is not None:
            q = q.filter_is_online(is_online)
        if is_active is not None:
            q = q.filter_is_active(is_active)
        return q

    def filter_is_online(self, is_online):
        neg = "" if is_online else "NOT"
        return self.extra(where=['''
            radcheck.username %s IN (
                SELECT username FROM radacct
                WHERE acctstoptime IS NULL
            )
            ''' %neg])

    def filter_is_active(self, is_active):
        neg = "NOT" if is_active else ""
        return self.extra(where=['''
            radcheck.username %s IN (
                SELECT rc.username FROM radcheck as rc 
                WHERE attribute='Auth-Type'
                      AND op=':='
                      AND value='Reject'
            )
            ''' %neg])

class RadUserManager(models.Manager):
    def get_query_set(self):
        return RadUserQuerySet(self.model).filter(attribute='User-Password', op=':=')

    def create(self, **kwargs):
        if 'password' in kwargs:
            kwargs['value'] = kwargs['password']
            del kwargs['password']
        kwargs.update(dict(attribute='User-Password', op=':='))
        return super(RadUserManager, self).create(**kwargs)

    def get_or_create(self, **kwargs):
        if 'defaults' not in kwargs:
            kwargs['defaults'] = {}
        #query by password is not useful
        #if 'password' in kwargs:
        #    kwargs['value'] = kwargs['password']
        #    del kwargs['password']
        kwargs['defaults'].update(dict(attribute='User-Password', op=':='))
        if 'password' in kwargs['defaults']:
            kwargs['defaults']['value'] = kwargs['defaults']['password']
            del kwargs['defaults']['password']
        return super(RadUserManager, self).get_or_create(**kwargs)
 
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
        

class RadUser(Radcheck):
    objects = RadUserManager()

    class Meta:
        proxy = True

    @property
    def is_online(self):
        return Radacct.objects.filter(
            username=self.username,
            acctstoptime=None).exists()
 
    def get_password(self):
        return self.value

    def set_password(self, password):
        self.value = password
        self.save()

    password = property(get_password, set_password)

    def get_is_active(self):
        return not Radcheck.objects.filter(
            username=self.username,
            attribute='Auth-Type',
            op=':=',
            value='Reject').exists()

        return not self.is_suspended

    def set_is_active(self, is_active):
        username = self.username
        if not is_active:
            Radcheck.objects.get_or_create(username=username, attribute='Auth-Type', op=':=', value='Reject')
        else:
            Radcheck.objects.filter(username=username, attribute='Auth-Type', op=':=', value='Reject').delete()

    is_active = property(get_is_active, set_is_active)

    def get_groups(self):
        return (Radusergroup.objects
            .filter(username=self.username)
            .order_by('priority')
            .values_list('groupname', flat=True)
            )
 
    def set_groups(self, groups):
        username = self.username
        old_groups = self.groups
        if old_groups != groups:
            to_delete = set(old_groups) - set(groups)
            Radusergroup.objects.filter(username=username, groupname__in=to_delete).delete()

            for p, group in enumerate(groups):
                rup,created = Radusergroup.objects.get_or_create(username=username, groupname=group, defaults={'priority':p})
                rup.priority = p
                rup.save()

    groups = property(get_groups, set_groups)

    def update(self, password=None, is_active=None, groups=None):
        #update password 
        record = self
        if password is not None and record.value != password:
            self.set_password(password)

        #update valid state
        if is_active is not None:
            self.set_is_active(is_active)

        #update groups 
        if groups is not None and type(groups) in (list, tuple):
            self.set_groups(groups)


def get_radgroup_count():
    groups = list(Radusergroup.objects.values_list('groupname', flat=True).distinct())
    groups += list(Radgroupcheck.objects.values_list('groupname', flat=True).distinct())

    return len(set(groups))

def get_groups():
    groups = list(Radusergroup.objects.values_list('groupname', flat=True).distinct())
    groups += list(Radgroupcheck.objects.values_list('groupname', flat=True).distinct())
    groups = set(groups)
    return [RadGroup(groupname) for groupname in groups]


def get_group(groupname):
    gs = Radgroupcheck.objects.filter(groupname=groupname)
    if gs.count() > 0:
        return RadGroup(groupname)
    gs = Radusergroup.objects.filter(groupname=groupname)
    if gs.count() > 0:
        return RadGroup(groupname)
   
class RadGroup(object):

    def __init__(self, groupname=None, attrs=None):
        self.groupname = groupname
        self.attrs = attrs

    @property
    def simultaneous_use(self):
        try:
            return Radgroupcheck.objects.get(groupname=self.groupname,
                attribute='Simultaneous-Use', op=':=').value
        except Radgroupcheck.DoesNotExist:
            return None
            
    def set_simultaneous_use(self, su):
        radg, created = Radgroupcheck.objects.get_or_create(
            groupname=self.groupname,
            attribute='Simultaneous-Use', op=':=',
            defaults={'value' : su})

        if not created:
            radg.value = su
            radg.save()

    @property
    def user_count(self):
        return Radusergroup.objects.filter(groupname=self.groupname).values('username').distinct().count()

