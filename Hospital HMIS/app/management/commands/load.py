"""
 ©Copyright 2018 Ministry of Health, Government of the Republic of Zambia.

 This File is part of MFL

 MFL is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.


 @package MFL
 @subpackage
 @access public
 @author Chisanga L. Siwale<chisanga.siwaled@moh.gov.zm>
 @copyright Copyright &copy; 2018, Ministry of Health, Government of the Republic of Zambia.
 @version Demo-v2.a
"""

__author__ = "Chisanga L. Siwale"
__copyright__ = "©Copyright 2018 Ministry of Health, Government of the Republic of Zambia"
__credits__ = []
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Chisanga L. Siwale"
__email__ = "chisanga.siwaled@moh.gov.zm"
__status__ = "Production"


import os
import logging
from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand, CommandError
from MFL.models import *
from geography.models import *


""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run(self, options['mode'])
        self.stdout.write('done.')


provinces_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../geography/data', 'Province.shp'),
)

districts_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../geography/data/Districts', 'Districts.shp'),
)

constituencies_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../geography/data/Constituencies', 'Constituencies.shp'),
)

wards_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../geography/data', 'Ward.shp'),
)

facility_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../../geography/data', 'Facility.shp'),
)

# Auto-generated `LayerMapping` dictionary for Province model
province_mapping = {
    'name': 'NAME',
    'population': 'POPULATION',
    'pop_density': 'POP_DENSIT',
    'area_sq_km': 'AREA_SQ_KM',
    'geom': 'MULTIPOLYGON',
}


# Auto-generated `LayerMapping` dictionary for District model
district_mapping = {
    'name': 'NAME',
    'district_type': {'name': 'FEATURE_TY'},
    'province': {'name': 'PROVINCE'},
    'population': 'POPULATION',
    'pop_density': 'POP_DENSIT',
    'area_sq_km': 'AREA_SQ_KM',
    'geom': 'MULTIPOLYGON',
}


# Auto-generated `LayerMapping` dictionary for Constituency model
constituency_mapping = {
    'name': 'NAME',
    'district': {'name': 'DISTRICT'},
    'population': 'POPULATION',
    'pop_density': 'POP_DENSIT',
    'area_sq_km': 'AREA_SQ_KM',
    'geom': 'MULTIPOLYGON',
}


# Auto-generated `LayerMapping` dictionary for Ward model
ward_mapping = {
    'name': 'NAME',
    'population': 'POPULATION',
    'pop_density': 'POP_DENSIT',
    'area_sq_km': 'AREA_SQ_KM',
    'geom': 'MULTIPOLYGON',
}


# Auto-generated `LayerMapping` dictionary for Facility model
facility_mapping = {
    'DHIS2_UID': 'DHIS2_UID',
    'smartcare_GUID': 'smartcare_',
    'iHRIS_ID': 'iHRIS_ID',
    'district': {'name': 'district'},
    'name': 'name',
    'HMIS_code': 'HMIS_code',
    'location_type': {'name': 'location'},
    'ownership': {'name': 'ownership'},
    'facility_type': {'name': 'facility_t'},
    'catchment_population_head_count': 'catchment_',
    'catchment_population_cso': 'catchmen_1',
    'longitude': 'longitude',
    'latitude': 'latitude',
    'operation_status': {'name': 'operation_'},
    'geom': 'Point',
}


def load_operational_status_table():
    logging.info('Starting loading OperationalStatus table...\n')

    data = {
        'Operational': 'A facility that is open and serving patients',
        'Licensed': 'A facility that has been approved and issued a license by the appropriate national regulatory '
                    'body, but facility is not yet operational.',
        'Pending Licensing': 'A facility that has been recommended by the district health management team, '
                             'but is waiting for a license from the national regulatory body.',
        'License Suspended': 'A facility whose license has been temporarily stopped for reasons including '
                             'selfrequest, sickness, disciplinary action, etc.',
        'License Cancelled': 'A facility whose license has been permanently stopped by the national body.',
        'Pending Registration': 'A facility that has been approved by the local authorities as an institution and a '
                                'request for official registration have been submitted and with approval pending.',
        'Registered': 'A facility that has been approved as an institution and a registration number given.',
        'Closed': 'A facility that has a valid license, but which has permanently closed.',
        'Invalid': 'A facility where the attributes of a facility (name, location, etc.) are different than those on '
                   'the facility’s license.',
        'Does not exist': 'A facility which has been licensed, but has been verified not to physically exist.',
        'Duplicate': 'The facility exists and is properly licensed, but is an effective duplicate of another '
                     'facility. This usually occurs when two data sources are merged together, with slightly '
                     'different names but refer to the same facility.',
        'Under Construction': ' '
    }

    try:
        for status, desc in data.items():
            OperationStatus.objects.create(name=status, description=desc)
            logging.info('Saved: OperationalStatus => ' + status)
    except Exception as e:
        logging.info(str(e))

    logging.info('Completed loading OperationalStatus table!\n')


def load_ownership_table():
    logging.info('Starting loading ownership table...\n')
    data = ['GRZ', 'Private', 'NGO', 'Police', 'Military', '']

    try:
        for ownership in data:
            Ownership.objects.create(name=ownership)
            logging.info('Saved: Ownership => '+ownership)
    except Exception as e:
        logging.info(str(e))

    logging.info('Completed loading ownership table!\n')


# Load MFL facility type model
def load_facility_type_table():
    logging.info('Starting loading FacilityType table...\n')

    data = [
        'Health Post',
        'Border Health Post',
        'Rural Health Centre',
        'Urban Health Centre',
        'Zonal Health Centre',
        'Hospital Affiliated Health Centre',
        'Hospital - Level 1',
        'Hospital - Level 2',
        'Hospital - Level 3',
        'Police',
        'Military',
        'Private',
        'NGO',
        '',
    ]

    try:
        for facility_type in data:
            FacilityType.objects.create(name=facility_type)
            logging.info('Saved: FacilityType => ' + facility_type)
    except Exception as e:
        logging.error(str(e))

    logging.info('Completed loading FacilityType table!\n')


# Loads table MFL_servicecategory
def load_service_category_table():
    logging.info('Starting loading ServiceCategory table!\n')

    data = ['Accident and Emergency Casualty Service',
            'Ambulatory Services',
            'Antenatal Care',
            'Blood Transfusion Services',
            'Curative Services',
            ]

    try:
        for service_category in data:
            ServiceCategory.objects.create(name=service_category)
            logging.info('Saved: ServiceCategory => '+service_category)
    except Exception as e:
        logging.info(str(e))

    logging.info('Completed loading ServiceCategory table!\n')


# Loads table geography_districttype
def load_district_type_table():
    logging.info('Starting loading DistrictType table!\n')

    data = ['City', 'Provincial Town', 'District Town']

    try:
        for district_type in data:
            DistrictType.objects.create(name=district_type)
            logging.info('Saved: DistrictType => ' + district_type)
    except Exception as e:
        logging.error(str(e))

    logging.info('Completed loading DistrictType table!\n')


def load_location_type_table():
    logging.info('Starting loading LocationType table..\n')

    try:
        data = ['Urban', 'Peri-Urban', 'Rural', '']
        for location_type in data:
            LocationType.objects.create(name=location_type)
            logging.info('Saved: LocationType => ' + location_type)
    except Exception as e:
        logging.error(str(e))

    logging.info('Completed loading LocationType table!\n')


def load_operating_hours_table():
    logging.info('Starting loading OperatingHours table...\n')

    try:
        data = ['Open whole day', 'Open 24hrs', 'Open weekends', 'Open public holidays']
        for operating_hour_type in data:
            OperatingHours.objects.create(name=operating_hour_type)
            logging.info('Saved: OperatingHours => ' + operating_hour_type)
    except Exception as e:
        logging.error(str(e))

    logging.info('Completed loading OperatingHours table!\n')


# def transform_district_table():
#     District.objects.all().update(name=_name.upper())


# def load_provinces(apps, schema_editor):
#     with open('geography/data/data.csv') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         # csv_reader = csv.DictReader(csvfile)
#
#         line_count = 0
#         output_rows = []
#
#         next(csv_reader)
#
#         for row in csv_reader:
#             # province = Province(name=row['name'], population=row['population'], pop_density=row['pop_density'],
#             # area_sq_km=row['area_sq_km']) province.save()
#             Province.objects.create(name=row[0], population=row[1], pop_density=row[2], area_sq_km=row[3], geom=row[4])


def update_wards_table():
    qs = Ward.objects.all()

    for ward in qs:
        constituent = Constituency.objects.filter(geom__contains=ward.geom)
        if constituent:
            ward.constituency = constituent[0]
            ward.save()
            logging.info('Saved: Ward ' + ward.name + ' => ' + constituent[0].name)


def update_facilities_table():
    qs = Facility.objects.all()

    for facility in qs:
        constituent = Constituency.objects.filter(geom__contains=facility.geom)
        ward = Ward.objects.filter(geom__contains=facility.geom)

        if constituent:
            facility.constituency = constituent[0]
            facility.save()
            logging.info('Saved: Facility ' + facility.name + ': Constituent => ' + constituent[0].name)

        if ward:
            facility.ward = ward[0]
            facility.save()
            logging.info('Saved: Facility ' + facility.name + ': Ward => ' + ward[0].name)


def clear_data():
    """Deletes all data tables"""
    logging.info("Clearing data...")
    Facility.objects.all().delete()
    FacilityType.objects.all().delete()
    Ownership.objects.all().delete()
    Ward.objects.all().delete()
    Constituency.objects.all().delete()
    District.objects.all().delete()
    DistrictType.objects.all().delete()
    Province.objects.all().delete()


def run(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:

    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    lm = LayerMapping(Province, provinces_shp, province_mapping, transform=False)
    lm.save(strict=True, verbose=True)

    load_district_type_table()

    lm = LayerMapping(District, districts_shp, district_mapping, transform=False)
    lm.save(strict=True, verbose=True)

    lm = LayerMapping(Constituency, constituencies_shp, constituency_mapping, transform=False)
    lm.save(strict=False, verbose=True)

    lm = LayerMapping(Ward, wards_shp, ward_mapping, transform=False)
    lm.save(strict=True, verbose=True)

    load_facility_type_table()
    load_operational_status_table()

    load_ownership_table()
    load_location_type_table()

    # try:
    #     lm = LayerMapping(Facility, facility_shp, facility_mapping, transform=False)
    #     lm.save(strict=False, verbose=True)
    # except Exception as e:
    #     logging.error('Import error: '.format(e))

    lm = LayerMapping(Facility, facility_shp, facility_mapping, transform=False)
    lm.save(strict=False, verbose=True)

    update_wards_table()

    update_facilities_table()
