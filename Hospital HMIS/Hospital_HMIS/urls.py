"""
Definition of urls for Hospital_HMIS.
"""

from datetime import datetime
from django.urls import path
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
    path('OPDEvents', views.OPDEventList.as_view(), name='opd_event_list'),
    path('OPDEvent/<int:pk>', views.OPDEventDetail.as_view(), name='opd_event_detail'),
    path('create', views.OPDEventCreate.as_view(), name='opd_event_create'),
    path('update/<int:pk>', views.OPDEventUpdate.as_view(), name='opd_event_update'),
    path('delete/<int:pk>', views.OPDEventDelete.as_view(), name='opd_event_delete'),
]
