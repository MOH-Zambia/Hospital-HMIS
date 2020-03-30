"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from app.models import OPDEvent, ICD10

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class OPDEventForm(forms.ModelForm):

    class Meta:  
        model = OPDEvent 
        fields = "__all__" 
        #fields = ['reference_number', 'age_in_days', 'age_in_months', 'age_in_years', 'location', 
        #          'gender', 'diagnosis', 'secondary_diagnosis', 'other_diagnosis', 'referred_from', 'referred_to', 'event_completed', 'comments']
        
        GENDER_CHOICES = [('M','Male'),('F','Female')]

        widgets = {
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def send_event(self):
        # send email using the self.cleaned_data dictionary
        pass


    def clean_diagnosis(self):

        if self.cleaned_data['diagnosis'].strip():
            q = self.cleaned_data['diagnosis']
            q  = q.split()[1:]

            print(q)

            description = ICD10.objects.filter(description=q)

        if not description:
            raise forms.ValidationError("Invalid ICD10 Code")
        return q
        