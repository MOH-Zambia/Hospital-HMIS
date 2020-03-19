"""
Definition of models.
"""

from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=64, unique=True)

    # Returns the string representation of the model.
    def __str__(self):  # __unicode__ on Python 2
        return self.name


class DistrictType(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = "District Types"


class LocationType(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = "Location Types"


class District(models.Model):
    name = models.CharField(max_length=30, unique=True)
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    district_type = models.ForeignKey(DistrictType, on_delete=models.DO_NOTHING)

    def get_province(self):
        return self.province.name

    # Returns the string representation of the model.
    def __str__(self):  # __unicode__ on Python 2
        return self.name


class SearchManager(models.Manager):
    def search(self, **kwargs):
        query_string = ''
        qs = self.all()

        if kwargs.get('form_data').get('name', ''):
            qs = qs.filter(name__icontains=kwargs['form_data']['name'])
            query_string += '&name=' + kwargs['form_data']['name']
        if kwargs.get('form_data').get('facility_type', []):
            qs = qs.filter(facility_type=kwargs['form_data']['facility_type'])
            query_string += '&facility_type=' + kwargs['form_data']['facility_type']


        return {
            'query_set': qs,
            'query_string': query_string
        }


class FacilityType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = "Facility Types"


class Facility(models.Model):
    DHIS2_UID = models.CharField(max_length=13, null=True, blank=True)
    HMIS_code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100)
    facility_type = models.ForeignKey(FacilityType, on_delete=models.DO_NOTHING)
    district = models.ForeignKey(District, on_delete=models.DO_NOTHING)
    location_type = models.ForeignKey(LocationType, on_delete=models.DO_NOTHING, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    slug = models.SlugField(max_length=254, null=True, blank=True)

    def province(self):
        return self.district.province.name

    def __str__(self):  # __unicode__ on Python 2
        return "%s | %s" % (self.HMIS_code, self.name)

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    # objects = FacilityManager()

    def get_absolute_url(self):  # get_absolute_url
        # return f"/facility/{self.slug}"
        return reverse('facility', kwargs={'pk': self.id})

    @property
    def title(self):
        return self.name

    objects = SearchManager()


class ICD10(models.Model):
    name = models.CharField(max_length=100, unique=True)
    uid = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)
    option = models.CharField(max_length=100, unique=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    class Meta:
        verbose_name_plural = "ICD10 Codes"


class OPDEvent(models.Model):
    reference_number = models.CharField(max_length=100, unique=True)
    date_of_birth = models.DateField()
    age_in_days = models.IntegerField()
    age_in_months = models.IntegerField()
    age_in_years = models.IntegerField()
    report_date = models.DateField(auto_now_add=True, auto_now=False)
    data_of_attendance = models.DateField()
    location = models.CharField(max_length=120, blank=True)
    gender = models.CharField(max_length=1)
    diagnosis = models.ForeignKey(ICD10, on_delete=models.DO_NOTHING)
    secondary_diagnosis = models.ForeignKey(ICD10, related_name='secondary_diagnosis', on_delete=models.DO_NOTHING)
    other_diagnosis = models.ForeignKey(ICD10, related_name='other_diagnosis', on_delete=models.DO_NOTHING, blank=True)
    # referred_from = models.ForeignKey(Facility, on_delete=models.DO_NOTHING, blank=True)
    # referred_to = models.ForeignKey(Facility, on_delete=models.DO_NOTHING, blank=True)
    referred_from = models.CharField(max_length=120, blank=True)
    referred_to = models.CharField(max_length=120, blank=True)
    event_completed = models.BooleanField()
    comments = models.TextField(null=True, blank=True)

    def __str__(self):  # __unicode__ on Python 2
        return self.reference_number

    def get_absolute_url(self):
        return reverse('opd_event_detail', args=[str(self.id)])

    class Meta:
        verbose_name_plural = "OPD 1st Attendance Events"
