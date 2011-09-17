from django import forms
from django.utils.translation import ugettext_lazy as _

class RadUserFilterForm(forms.Form):
    username = forms.CharField(required=False)
    is_suspended = forms.ChoiceField(choices=[('-1', 'Any'), ('0', 'Active'), ('1', 'Suspended')], initial="-1")
    #group = forms.CharField(required=False)
