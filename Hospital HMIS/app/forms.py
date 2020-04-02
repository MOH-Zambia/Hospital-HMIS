"""
Definition of forms.
"""

from datetime import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from app.models import ICD10, OPDEvent, IPDEvent

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


    #def clean_date_of_birth(self):
    #    date_of_birth = self.cleaned_data['date_of_birth']
    #    if date_of_birth:
    #        try:
    #            date_of_birth = datetime.strptime(date_of_birth, '%d/%m/%Y')
    #            print('The date {} is valid.'.format(date_of_birth))
    #        except ValueError:
    #            msg = 'The date {} is invalid'.format(date_of_birth)
    #            print(msg)
    #            raise forms.ValidationError(msg)
    #    return date_of_birth


    #def clean_diagnosis(self):
    #
    #    if self.cleaned_data['diagnosis'].strip():
    #        q = self.cleaned_data['diagnosis']
    #        q  = " ".join(q.split()[1:-1])
    #
    #        print(q)
    #
    #        description = ICD10.objects.filter(description=q)
    #
    #    if not description:
    #        msg = "Invalid ICD10 Code"
    #        raise forms.ValidationError(msg)
    #        self.add_error('diagnosis', msg)
    #    return q


class IPDEventForm(forms.ModelForm):

    class Meta:  
        model = IPDEvent 
        fields = "__all__" 
        
        GENDER_CHOICES = [('M','Male'),('F','Female')]

        widgets = {
            'gender': forms.RadioSelect(choices=GENDER_CHOICES),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def send_event(self):
        # send email using the self.cleaned_data dictionary
        pass


