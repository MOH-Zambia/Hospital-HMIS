from django.contrib import admin 
from .models import *

admin.site.register(Province)
admin.site.register(District)
admin.site.register(LocationType)
admin.site.register(FacilityType)
admin.site.register(Facility)
admin.site.register(ICD10)
admin.site.register(OPDEvent)
admin.site.register(SeparationMode)
admin.site.register(IPDEvent)
