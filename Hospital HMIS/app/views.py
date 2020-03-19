"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext

from app.models import OPDEvent
from app.forms import OPDEventForm

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

class OPDEventList(ListView):
    template_name = 'app/events/opd_event_list.html'
    model = OPDEvent
    
    def get_context_data(self, **kwargs):
        context = super(OPDEventList, self).get_context_data(**kwargs)
        context['title'] = 'OPD 1st Attendance Cases'
        #context['reference_number'] = datetime.now().year
        return context


class OPDEventDetail(DetailView): 
    model = OPDEvent


class OPDEventCreate(CreateView):
    model = OPDEvent
    form_class = OPDEventForm
    fields = ( 'reference_number', 'date_of_birth', 'age_in_days', 'age_in_months', 'age_in_years', 'date_of_attendance', 'report_date',
        'location', 'gender', 'diagnosis', 'secondary_diagnosis', 'other_diagnosis', 'referred_from', 'referred_to', 'event_completed', 'comments', )
    success_url = '/'
    template_name = 'app/events/opd_event.html'

    def form_valid(self, form):
        # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
        form.instance.reference_number = self.cleaned_data['reference_number']
        form.instance.date_of_birth = self.cleaned_data['date_of_birth']
        form.instance.age_in_days = self.cleaned_data['age_in_days']
        form.instance.age_in_months = self.cleaned_data['age_in_months'] 
        form.instance.age_in_years = self.cleaned_data['age_in_years']
        form.instance.date_of_attendance = self.cleaned_data['date_of_attendance']
        form.instance.report_date = self.cleaned_data['report_date']
        form.instance.location = self.cleaned_data['location']
        form.instance.gender = self.cleaned_data['gender']
        form.instance.diagnosis = self.cleaned_data['diagnosis']
        form.instance.secondary_diagnosis = self.cleaned_data['secondary_diagnosis']
        form.instance.other_diagnosis = self.cleaned_data['other_diagnosis']
        form.instance.referred_from = self.cleaned_data['referred_from']
        form.instance.referred_to = self.cleaned_data['referred_to']
        form.instance.event_completed = self.cleaned_data['event_completed']
        form.instance.comments = self.cleaned_data['comments']

        #Send event to dhis2 instance
        #form.send_event()

        return super().form_valid(form)


class OPDEventUpdate(UpdateView): 
    model = OPDEvent


class OPDEventDelete(DeleteView): 
    model = OPDEvent


@login_required
def seed(request):
    """Seeds the database with sample polls."""
    facility_list_path = path.join(path.dirname(__file__), 'Facility_List.json')
    with open(facility_list_path, 'r') as facility_list_file:
        facilities = json.load(facility_list_file)

    for facility in facilities:
        facility = Facility()
        facility.facility_id = facility['facility_id']
        facility.name = facility['name']
        facility.save()



    return HttpResponseRedirect(reverse('app:home'))