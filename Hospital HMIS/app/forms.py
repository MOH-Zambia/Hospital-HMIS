"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from app.models import ICD10

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


class OPDEventForm(forms.Form):
    GENDER_CHOICES = [('M','Male'),('F','Female')]

    reference_number = forms.CharField(max_length=100, required=True, widget=forms.TextInput)
    date_of_birth = forms.DateField()
    age_in_days = forms.IntegerField()
    age_in_months = forms.IntegerField()
    age_in_years = forms.IntegerField()
    date_of_attendance = forms.DateField()
    report_date = forms.DateField()
    location = forms.CharField(max_length=120, required=False, widget=forms.TextInput)
    gender = forms.CharField(label='Gender', widget=forms.RadioSelect(choices=GENDER_CHOICES))
    diagnosis = forms.ModelChoiceField(required=True, queryset=ICD10.objects.all(), empty_label="Select primary diagnosis...")
    secondary_diagnosis = forms.ModelChoiceField(required=False, queryset=ICD10.objects.all(), empty_label="Select secondary diagnosis...")
    other_diagnosis = forms.ModelChoiceField(required=False, queryset=ICD10.objects.all(),  empty_label="Select other diagnosis...")
    referred_from = forms.CharField()
    referred_to = forms.CharField()
    event_completed = forms.BooleanField()
    comments = forms.Textarea()

    def clean_report_date(self):
        data = self.cleaned_data['report_date']
        date_of_attendance = self.cleaned_data['date_of_attendance']
        
        # Check if a date is after date_of_attendance. 
        if data >= date_of_attendance:
            raise ValidationError(_('Invalid report date - Report date should be after date of attendance'))

        # Remember to always return the cleaned data.
        return data

    def send_event(self):
        # send email using the self.cleaned_data dictionary
        pass
