from django import forms
from django.utils.translation import ugettext_lazy as _

class RadUserFilterForm(forms.Form):
    username = forms.CharField(required=False)
    is_active = forms.ChoiceField(choices=[('-1', 'Any'), ('1', 'Active'), ('0', 'Suspended')], initial="-1")
    is_online = forms.ChoiceField(choices=[('-1', 'Any'), ('0', 'Offline'), ('1', 'Online')], initial="-1")
    #group = forms.CharField(required=False)


class RadUserForm(forms.Form):
    username = forms.RegexField(r'^[0-9a-zA-Z\.@\-_]+$', 
                                widget=forms.TextInput(attrs={'readonly':'readonly'}),
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and .@-_ are allowed.')})
    password = forms.CharField(max_length=20)
    is_active = forms.BooleanField(required=False, initial=True)
    groups = forms.RegexField(r'^[0-9a-zA-Z\._,]+$', max_length=50, initial='default', required=False,
                             help_text=_('comma seprated group list, eg "default,test"'),
                             error_messages={'invalid' : _('Only letters, digests and ._ are allowed as group name.')})

    def clean_groups(self):
        data = self.cleaned_data['groups']
        data = u','.join([x for x in data.split(u',') if x])
        return data
 
class NewRadUserForm(RadUserForm):
    username = forms.RegexField(r'^[0-9a-zA-Z\.@\-_]+$', 
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and .@-_ are allowed.')})
 

class RadGroupForm(forms.Form):
    groupname = forms.RegexField(r'^[0-9a-zA-Z\-_]+$', 
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and -_ are allowed.')})
 
    simultaneous_use = forms.IntegerField(initial=1)


class NewRadGroupForm(RadGroupForm):
    groupname = forms.RegexField(r'^[0-9a-zA-Z\-_]+$', 
                                min_length=3, max_length=20, required=True,
                                error_messages={'invalid' : _('Only letters, digests and -_ are allowed.')})
