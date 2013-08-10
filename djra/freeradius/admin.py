# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin

from .models import Radpostauth
from .models import Radreply
from .models import Radusergroup
from .models import Radcheck
from .models import Radgroupcheck
from .models import Radgroupreply
from .models import Radippool
from .models import Radacct

class RadpostauthAdmin(admin.ModelAdmin):
    pass

class RadreplyAdmin(admin.ModelAdmin):
    list_display   = ('calledstationid', 'custid', 'username', 'attribute', 'op', 'value',)
    list_filter    = ('calledstationid', 'custid', 'username',)
    search_fields  = ('attribute', 'value',)

class RadusergroupAdmin(admin.ModelAdmin):
    list_display   = ('groupname', 'username',)
    list_filter    = ('groupname',)
    search_fields  = ('username',)

class RadcheckAdmin(admin.ModelAdmin):
    list_display   = ('username', 'attribute', 'op', 'value',)
    list_filter    = ('username',)
    search_fields  = ('attribute', 'value',)

class RadgroupcheckAdmin(admin.ModelAdmin):
    list_display   = ('groupname', 'attribute', 'op', 'value',)
    list_filter    = ('groupname',)

class RadgroupreplyAdmin(admin.ModelAdmin):
    list_display   = ('groupname', 'attribute', 'op', 'value',)
    list_filter    = ('groupname',)

class RadippoolAdmin(admin.ModelAdmin):
    list_display   = ('pool_name', 'framedipaddress', 'nasipaddress', 'expiry_time',)
    list_filter    = ('pool_name', 'nasipaddress', 'expiry_time',)
    search_fields  = ('framedipaddress',)

class RadacctAdmin(admin.ModelAdmin):
    list_display   = ('acctuniqueid', 'username', 'nasipaddress', 'acctstarttime', 'acctsessiontime',)
    list_filter    = ('nasipaddress',)


admin.site.register(Radpostauth,RadpostauthAdmin)
admin.site.register(Radreply,RadreplyAdmin)
admin.site.register(Radusergroup,RadusergroupAdmin)
admin.site.register(Radcheck,RadcheckAdmin)
admin.site.register(Radgroupcheck,RadgroupcheckAdmin)
admin.site.register(Radgroupreply,RadgroupreplyAdmin)
admin.site.register(Radippool,RadippoolAdmin)
admin.site.register(Radacct,RadacctAdmin)

if getattr(settings, 'FREERADIUS_ENABLE_EXT_MODELS', False):
    from .models import Attributelist
    from .models import Nas
    from .models import Realmgroup
    from .models import Realms


    class AttributelistAdmin(admin.ModelAdmin):
        list_display   = ('attribute', 'enabled', 'checkitem',)
        list_filter    = ('enabled', 'checkitem',)
        ordering       = ('attribute', )
        search_fields  = ('attribute',)

    class NasAdmin(admin.ModelAdmin):
        list_display   = ('nasname', 'shortname', 'type', 'ports', 'naslocation',)
        list_filter    = ('type', 'naslocation',)
        ordering       = ('nasname', )
        search_fields  = ('nasname', 'shortname', 'ports', 'naslocation',)


    class RealmgroupAdmin(admin.ModelAdmin):
        pass

    class RealmsAdmin(admin.ModelAdmin):
        pass

    admin.site.register(Attributelist,AttributelistAdmin)
    admin.site.register(Nas,NasAdmin)
    admin.site.register(Realmgroup,RealmgroupAdmin)
    admin.site.register(Realms,RealmsAdmin)
