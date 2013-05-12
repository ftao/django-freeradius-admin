import random
import string
import itertools
from tastypie.resources import ModelResource,Resource
from tastypie import fields,bundle
from tastypie.exceptions import NotFound

from .models import RadUser,Radgroupcheck,RadGroup

def gen_random_password(len):
    return ''.join(random.choice(string.digits) for i in xrange(len))

class RadUserResource(ModelResource):
    password = fields.CharField(attribute='password', readonly=True)
    is_active = fields.BooleanField(attribute='is_active')
    is_online = fields.BooleanField(attribute='is_online')
    groups = fields.ListField(attribute='groups')

    class Meta:
        queryset = RadUser.objects.all()
        resource_name = 'raduser'
        fields = ['username', 'password', 'is_active', 'is_online', 'groups']
        filtering = {
            "username": ('exact',),
            "is_online" : ('exact',),
            "is_active" : ('exact',)
        }


    def obj_create(self, bundle, **kwargs):
        data = bundle.data
        if 'password' not in data:
            data['password'] = gen_random_password(6)

        raduser = RadUser.objects.create(username=data['username'], password=data['password'])
        update = {k:data[k] for k in data if k not in ('username', 'password')}
        raduser.update(**update)

        return raduser

    def obj_update(self, bundle, **kwargs):
        data = bundle.data
        raduser,created = RadUser.objects.get_or_create(username=data['username'])
        update = {k:data[k] for k in data if k not in ('username',)}
        raduser.update(**update)
        bundle.obj = raduser

        return raduser


class RadGroupResource(Resource):
    groupname = fields.CharField(attribute='groupname')
    attrs = fields.ListField(attribute='attrs')

    class Meta:
        resource_name = 'radgroup'
        object_class = RadGroup
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, bundle.Bundle):
            kwargs['pk'] = bundle_or_obj.obj.groupname
        else:
            kwargs['pk'] = bundle_or_obj.groupname

        return kwargs

    def get_object_list(self, request):
        return self.obj_get_list()

    def obj_get_list(self, bundle=None, **kwargs):
        radgc_records =  Radgroupcheck.objects.all().order_by('groupname')
        groups = []
        for g, rows in itertools.groupby(radgc_records, lambda x: x.groupname):
            groups.append(self._build_group(g, list(rows)))
        return groups

    def obj_get(self, bundle, **kwargs):
        groupname = kwargs.get('pk') 
        radgc_records =  Radgroupcheck.objects.filter(groupname=groupname)
        if len(radgc_records) == 0:
            raise NotFound
        return self._build_group(groupname, radgc_records)

    def _build_group(self, groupname, radgc_records):
        attrs = []
        for radgc in radgc_records:
            attrs.append({'attribute' : radgc.attribute,
                            'op' : radgc.op,
                            'value' : radgc.value})
        return RadGroup(groupname, attrs)
