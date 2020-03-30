"""
Definition of urls for Hospital_HMIS.
"""

from datetime import datetime
from django.urls import path
from django.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # url(r"^autocomplete/", include("autocomplete_light.urls")),
    path('admin/', admin.site.urls),
    
    #path('OPDEvents', views.OPDEventList.as_view(), name='opd_event_list'),
    #path('OPDEvent/<int:pk>', views.OPDEventDetail.as_view(), name='opd_event_detail'),

    path('create_opd_event', views.create_opd_event),
    path('list_opd_events', views.list_opd_events),  
    path('edit_opd_event/<int:id>', views.edit_opd_event),  
    path('update_opd_event/<int:pk>', views.update_opd_event),
    path('delete_opd_event/<int:pk>', views.delete_opd_event),

    path('autocomplete_icd10_diagnosis', views.autocomplete_icd10_diagnosis),
    path('export_csv', views.export_csv),
]
