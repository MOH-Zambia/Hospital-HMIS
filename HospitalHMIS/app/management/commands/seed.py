__author__ = 'Chisanga L. Siwale <chisanga.siwale@moh.gov.zm>'

import csv
import logging
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django_seed import Seed
import json

from app.models import *


seeder = Seed.seeder()
FACILITY_FILENAME = 'data/Facility.json'
FACILITY_TYPE_FILENAME = 'data/Facility_Types.json'
LOCATION_TYPE_FILENAME = 'data/Location_Types.json'
DISTRICT_FILENAME = 'data/District.json'
PROVINCE_FILENAME = 'data/Province.json'
ICD10_FILENAME = 'data/ICD10.json'
DHIS2_ICD10_FILENAME = 'data/DHIS2_ICD10.csv'
SEPARATION_MODE_FILENAME = 'data/Separation_Modes.json'

facility_path = Path(__file__).parents[3] / FACILITY_FILENAME
facility_type_path = Path(__file__).parents[3] / FACILITY_TYPE_FILENAME
location_type_path = Path(__file__).parents[3] / LOCATION_TYPE_FILENAME
district_path = Path(__file__).parents[3] / DISTRICT_FILENAME
province_path = Path(__file__).parents[3] / PROVINCE_FILENAME
icd10_path = Path(__file__).parents[3] / ICD10_FILENAME
dhis2_icd10_path = Path(__file__).parents[3] / DHIS2_ICD10_FILENAME
separation_mode_path = Path(__file__).parents[3] / SEPARATION_MODE_FILENAME

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

        # Optional argument
        parser.add_argument('-t', '--table', type=str, help='Define which table to seed', )

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run(self, options)
        self.stdout.write('done.')


def seed_icd10():
    """Creates a icd10 object from json file"""
    logging.info("Loading icd10 codes...")
    
    with open(facility_icd10_path, 'r') as icd10_file:
        icd10_codes = json.load(icd10_file)

    for icd10 in icd10_codes:
        icd10_code = ICD10()
        icd10_code.code = icd10['code']
        icd10_code.description = icd10['desc']
        icd10_code.save()


def seed_dhis2_icd10():
    with open(dhis2_icd10_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        line_count = 0
        output_rows = []

        next(csv_reader)

        for row in csv_reader:
            icd10_code = DHIS2_ICD10()
            icd10_code.udi = row[0]
            icd10_code.code = row[1]
            icd10_code.description = row[2]
            icd10_code.save()


def seed_facility_types():
    """Creates a facility type object from json file"""
    logging.info("Loading facility types...")
    
    with open(facility_type_path, 'r') as facility_type_file:
        facility_types = json.load(facility_type_file)

    for ft in facility_types:
        facility_type = FacilityType()
        facility_type.name = ft['name']
        facility_type.save()


def seed_location_types():
    """Creates a location type object from json file"""
    logging.info("Loading location types...")
    
    with open(location_type_path, 'r') as location_type_file:
        location_types = json.load(location_type_file)

    for l in location_types:
        location_type = LocationType()
        location_type.name = l['name']
        location_type.save()


def seed_provinces():
    """Creates a province object from json file"""
    logging.info("Loading provinces...")
    
    with open(province_path, 'r') as province_file:
        provinces = json.load(province_file)

    for p in provinces:
        province = Province()
        province.name = p['name']
        province.save()


def seed_districts():
    """Creates a district object from json file"""
    logging.info("Loading districts...")
    
    with open(district_path, 'r') as district_file:
        districts = json.load(district_file)

    for d in districts:
        district = District()
        district.name = d['name']
        district.province = Province.objects.get(name=d['province'])
        district.save()


def seed_facilities():
    """Creates a facility object from json file"""
    logging.info("Loading facilities...")
    
    with open(facility_path, 'r') as facility_file:
        facilities = json.load(facility_file)

    for f in facilities:
        facility = Facility()
        facility.facility_id = f['facility_id']
        facility.DHIS2_UID = f['DHIS2_UID']
        facility.HMIS_code = f['HMIS_code']
        facility.name = f['name']
        facility.facility_type = FacilityType.objects.get(name=f['facility_type'])
        facility.district = District.objects.get(name=f['district'])
        facility.location_type = LocationType.objects.get(name=f['location_type'])
        facility.slug = f['slug']
        facility.save()


def seed_separation_modes():
    """Creates a separation mode object from json file"""
    logging.info("Loading separation modes...")
    
    with open(separation_mode_path, 'r') as separation_mode_file:
        separation_modes = json.load(separation_mode_file)

    for s in separation_modes:
        separation_mode = SeparationMode()
        separation_mode.name = s['name']
        separation_mode.save()



def clear_data():
    """Deletes all the table data"""
    logging.info("Delete facility instances")
    Facility.objects.all().delete()
    logging.info("Delete district instances")
    District.objects.all().delete()
    logging.info("Delete province instances")
    Province.objects.all().delete()
    logging.info("Delete facility_type instances")
    FacilityType.objects.all().delete()
    logging.info("Delete location_type instances")
    LocationType.objects.all().delete()
    logging.info("Delete icd10 instances")
    ICD10.objects.all().delete()
    logging.info("Delete separation modes instances")
    SeparationMode.objects.all().delete()


def run(self, options):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    # clear_data()

    if options['mode'] == MODE_CLEAR:
        return

    #seed_facility_types()
    #seed_location_types()
    #seed_provinces()
    #seed_districts()
    #seed_facilities()
    #seed_icd10()
    seed_dhis2_icd10()
    #seed_separation_modes()




    
