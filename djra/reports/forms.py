from django import forms

class DateRangeForm(forms.Form):
    drange = forms.ChoiceField(
        choices=[
            ('today', 'Today'), 
            ('last-7', 'Last 7 Days'),
            ('last-30', 'Last 30 Days'),
        ],
        initial="today")

