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
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.template import RequestContext
import json
import csv
import sys
import collections

from app.models import OPDEvent, ICD10
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


def create_opd_event(request):  
    if request.method == "POST":  
        form = OPDEventForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                return redirect('app/events/list_opd_events')  
            except:  
                pass  
    else:  
        form = OPDEventForm()  

    return render(
        request, 
        'app/events/create_opd_event.html', 
        {
            'form': form,
            'title': 'New OPD Event',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )  


def list_opd_events(request):  
    opd_events = OPDEvent.objects.all()  

    return render(
        request,
        "app/events/list_opd_events.html", 
        {
            'opd_events': opd_events,
            'title': 'List OPD Events',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )  


def edit_opd_event(request, id):  
    opd_event = OPDEvent.objects.get(id=id)  

    return render(
        request,
        'app/events/edit_opd_event.html', 
        {
            'opd_event': opd_event,
            'title': 'Edit OPD Event',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )  


def update_opd_event(request, id):  
    opd_event = OPDEvent.objects.get(id=id)  
    form = OPDEventForm(request.POST, instance = employee)  

    if form.is_valid():  
        form.save()  
        return redirect("app/events/list_opd_events")  

    return render(
        request, 
        'app/events/edit_opd_event.html', 
        {
            'opd_event': opd_event,
            'title': 'Update OPD Event',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )  


def delete_opd_event(request, id):  
    opd_event = OPDEvent.objects.get(id=id)  
    opd_event.delete()  

    return redirect("app/events/list_opd_events")  


def autocomplete_icd10_diagnosis(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = ICD10.objects.filter(description__startswith=q)
        results = []
        print(q)

        for r in search_qs:
            results.append(r.__str__())
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def export_csv(request):
    opd_events = OPDEvent.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="OPD_1st_Attendance.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow([
            'reference_number',
            'date_of_birth',
            'age_in_days',
            'age_in_months',
            'age_in_years',
            'report_date',
            'date_of_attendance',
            'location',
            'gender',
            'diagnosis',
            'secondary_diagnosis',
            'other_diagnosis',
            'referred_from',
            'referred_to',
            'event_completed',
            'comments',]
        )

    for opd_event in opd_events:
         writer.writerow([
            opd_event.reference_number,
            opd_event.date_of_birth,
            opd_event.age_in_days,
            opd_event.age_in_months,
            opd_event.age_in_years,
            opd_event.report_date,
            opd_event.date_of_attendance,
            opd_event.location,
            opd_event.gender,
            opd_event.diagnosis,
            opd_event.secondary_diagnosis,
            opd_event.other_diagnosis,
            opd_event.referred_from,
            opd_event.referred_to,
            opd_event.event_completed,
            opd_event.comments,]
        )

    return response


def sync(request):
    # Get parameters from dish.json
    config = json.load(open('dhis2.json', 'r'))
    url = config['dhis']['baseurl'] + '/api/dataStore/assignments/organisationUnitLevels.json'

    # Get the current JSON from the organisationUnitLevels key of the assignments namespace in the data store
    credentials = (config['dhis']['username'], config['dhis']['password'])
    req = requests.get(url, auth=credentials)
    j = req.json()

    # Construct a new JSON from the current JSON, adding a new key and resorting it
    j['Python'] = j['Angola'].copy()
    j['Python']['name3'] = 'Python'
    k = sorted(j.items())

    # Since dicts don't have an order to their indices, 
    # we need to create an ordered dict and then 
    # save the sorted values to it

    l = collections.OrderedDict()
    for i in k:
	    l[i[0]] = i[1]

    # Replace the old JSON with the new JSON

    print(requests.put(url, data=json.dumps(l), auth=credentials, headers={'content-type': 'application/json'}))

    # Report completion and exit with status 0

    print('Exiting normally')


def load_districts(request):
    province_id = request.GET.get('province')
    districts = District.objects.filter(province_id=province_id).order_by('name')
    return render(request, 'app/district_dropdown_list_options_partial.html', {'districts': districts})


def load_diagnosis(request):
    if request.GET.get('q'):
        q = request.GET['q']
        data = model.objects.using('legacy').filter(email__startswith=q).values_list('email',flat=True)
        json = list(data)
        return JsonResponse(json, safe=False)

    else:
        HttpResponse("No cookies")


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