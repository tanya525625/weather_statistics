from django import forms
import cgi
 

class UserForm(forms.Form):
    city = forms.CharField()
    period_start = forms.DateField()
    period_end = forms.DateField()

