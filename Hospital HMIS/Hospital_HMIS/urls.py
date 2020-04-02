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
    path('admin/', admin.site.urls),

    path('create_opd_event', views.create_opd_event, name='create_opd_event'),
    path('list_opd_events', views.list_opd_events, name='list_opd_events'),  
    path('edit_opd_event/<int:pk>', views.edit_opd_event, name='edit_opd_event'),  
    path('delete_opd_event/<int:pk>', views.delete_opd_event, name='delete_opd_event'),

    path('create_ipd_event', views.create_ipd_event, name='create_ipd_event'),
    path('list_ipd_events', views.list_ipd_events, name='list_ipd_events'),  
    path('edit_ipd_event/<int:pk>', views.edit_ipd_event, name='edit_ipd_event'),  
    path('delete_ipd_event/<int:pk>', views.delete_ipd_event, name='delete_ipd_event'),

    path('autocomplete_icd10_diagnosis', views.autocomplete_icd10_diagnosis),
    path('export_opd_events', views.export_opd_events),
    path('export_ipd_events', views.export_ipd_events),
]
