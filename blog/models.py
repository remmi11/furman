# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

# class Post(models.Model):
#     author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(
#             default=timezone.now)
#     published_date = models.DateTimeField(
#             blank=True, null=True)

#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()

#     def __str__(self):
#         return self.title


class County(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Form(models.Model):
    date_entered = models.DateField(blank=True, null=True)
    date_needed = models.DateField(blank=True, null=True)
    client = models.CharField(max_length=50, blank=True, null=True)
    project_no = models.CharField(max_length=50, blank=True, null=True)
    map_no = models.CharField(max_length=10, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    certify_to = models.CharField(max_length=50, blank=True, null=True)
    lender = models.CharField(max_length=50, blank=True, null=True)
    gf_no = models.CharField(max_length=50, blank=True, null=True)
    address_street = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    survey_type = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    subdivision = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    sub_block = models.CharField(max_length=50, blank=True, null=True)
    lot = models.CharField(max_length=50, blank=True, null=True)
    survey = models.CharField(max_length=50, blank=True, null=True)
    rural_block = models.CharField(max_length=50, blank=True, null=True)
    rural_section = models.CharField(max_length=50, blank=True, null=True)
    meridian = models.CharField(max_length=10, blank=True, null=True)
    t_r = models.CharField(max_length=10, blank=True, null=True)
    plss_section = models.CharField(max_length=50, blank=True, null=True)
    folder_path = models.CharField(max_length=300, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    title1 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'form'


class Form500(models.Model):
    date_entered = models.DateField(blank=True, null=True)
    date_needed = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True)
    project_no = models.CharField(max_length=200, blank=True, null=True)
    map_no = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    certify_to = models.CharField(max_length=200, blank=True, null=True)
    lender = models.CharField(max_length=200, blank=True, null=True)
    gf_no = models.CharField(max_length=50, blank=True, null=True)
    address_street = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    survey_type = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    subdivision = models.CharField(max_length=200, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    sub_block = models.CharField(max_length=50, blank=True, null=True)
    lot = models.CharField(max_length=50, blank=True, null=True)
    survey = models.CharField(max_length=200, blank=True, null=True)
    rural_block = models.CharField(max_length=50, blank=True, null=True)
    rural_section = models.CharField(max_length=50, blank=True, null=True)
    meridian = models.CharField(max_length=10, blank=True, null=True)
    t_r = models.CharField(max_length=10, blank=True, null=True)
    plss_section = models.CharField(max_length=50, blank=True, null=True)
    folder_path = models.CharField(max_length=300, blank=True, null=True)
    prad_acct = models.CharField(max_length=50, blank=True, null=True)
    prad_acct_gis = models.CharField(max_length=50, blank=True, null=True)
    clerksfile = models.CharField(max_length=50, blank=True, null=True)
    book = models.CharField(max_length=50, blank=True, null=True)
    page = models.CharField(max_length=50, blank=True, null=True)
    filed = models.CharField(max_length=50, blank=True, null=True)
    surveyor = models.CharField(max_length=50, blank=True, null=True)
    canceled = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'form_500'


class FormAll(models.Model):
    date_entered = models.DateField(blank=True, null=True)
    date_needed = models.DateField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    client = models.CharField(max_length=200, blank=True, null=True)
    project_no = models.CharField(max_length=200, blank=True, null=True)
    map_no = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    certify_to = models.CharField(max_length=200, blank=True, null=True)
    lender = models.CharField(max_length=200, blank=True, null=True)
    gf_no = models.CharField(max_length=50, blank=True, null=True)
    address_street = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    survey_type = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    subdivision = models.CharField(max_length=200, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    sub_block = models.CharField(max_length=50, blank=True, null=True)
    lot = models.CharField(max_length=50, blank=True, null=True)
    survey = models.CharField(max_length=200, blank=True, null=True)
    rural_block = models.CharField(max_length=50, blank=True, null=True)
    rural_section = models.CharField(max_length=50, blank=True, null=True)
    meridian = models.CharField(max_length=10, blank=True, null=True)
    t_r = models.CharField(max_length=10, blank=True, null=True)
    plss_section = models.CharField(max_length=50, blank=True, null=True)
    folder_path = models.CharField(max_length=300, blank=True, null=True)
    prad_acct = models.CharField(max_length=50, blank=True, null=True)
    prad_acct_gis = models.CharField(max_length=50, blank=True, null=True)
    clerksfile = models.CharField(max_length=50, blank=True, null=True)
    book = models.CharField(max_length=50, blank=True, null=True)
    page = models.CharField(max_length=50, blank=True, null=True)
    filed = models.CharField(max_length=50, blank=True, null=True)
    surveyor = models.CharField(max_length=50, blank=True, null=True)
    canceled = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    volume = models.CharField(max_length=255, blank=True, null=True)
    requested_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'form_all'


class FurmanRecords(models.Model):
    prad_account_number = models.TextField(db_column='PRAD ACCOUNT NUMBER', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gispradaccount = models.TextField(db_column='GISPRADACCOUNT', blank=True, null=True)  # Field name made lowercase.
    records_pcreated = models.DateField(db_column='RECORDS_pCreated', blank=True, null=True)  # Field name made lowercase.
    records_pedited = models.DateField(db_column='RECORDS_pEdited', blank=True, null=True)  # Field name made lowercase.
    jobnumber = models.TextField(db_column='JobNumber', blank=True, null=True)  # Field name made lowercase.
    ap_field = models.TextField(db_column='AP#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    property_address = models.TextField(db_column='Property Address', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    requested_by = models.TextField(db_column='REquested By', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    section = models.TextField(db_column='Section', blank=True, null=True)  # Field name made lowercase.
    sectionastext = models.TextField(db_column='SECTIONASTEXT', blank=True, null=True)  # Field name made lowercase.
    olts_block = models.TextField(db_column='OLTS_BLOCK', blank=True, null=True)  # Field name made lowercase.
    olts_survey = models.TextField(db_column='OLTS_SURVEY', blank=True, null=True)  # Field name made lowercase.
    county = models.TextField(db_column='COUNTY', blank=True, null=True)  # Field name made lowercase.
    city_state = models.TextField(db_column='CITY_STATE', blank=True, null=True)  # Field name made lowercase.
    aka = models.TextField(db_column='AKA', blank=True, null=True)  # Field name made lowercase.
    clerks_file_number = models.TextField(db_column='Clerks File Number', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    platebook = models.TextField(db_column='PlateBook', blank=True, null=True)  # Field name made lowercase.
    platpage = models.TextField(db_column='PlatPage', blank=True, null=True)  # Field name made lowercase.
    block_sub = models.TextField(db_column='BLOCK_SUB', blank=True, null=True)  # Field name made lowercase.
    lot = models.TextField(db_column='Lot', blank=True, null=True)  # Field name made lowercase.
    filed = models.TextField(db_column='Filed', blank=True, null=True)  # Field name made lowercase.
    subdiv = models.TextField(db_column='Subdiv', blank=True, null=True)  # Field name made lowercase.
    taxmap = models.TextField(db_column='TaxMap', blank=True, null=True)  # Field name made lowercase.
    pnotes = models.TextField(db_column='pNotes', blank=True, null=True)  # Field name made lowercase.
    jobdesc = models.TextField(db_column='JobDesc', blank=True, null=True)  # Field name made lowercase.
    jobdate = models.TextField(db_column='JobDate', blank=True, null=True)  # Field name made lowercase.
    jobassig = models.TextField(db_column='JobAssig', blank=True, null=True)  # Field name made lowercase.
    requestedby = models.TextField(db_column='RequestedBy', blank=True, null=True)  # Field name made lowercase.
    jobcont = models.TextField(db_column='JobCont', blank=True, null=True)  # Field name made lowercase.
    jobphone = models.TextField(db_column='JobPhone', blank=True, null=True)  # Field name made lowercase.
    jobreq = models.TextField(db_column='JobReq', blank=True, null=True)  # Field name made lowercase.
    jobemail = models.TextField(db_column='JobEmail', blank=True, null=True)  # Field name made lowercase.
    jobaddres = models.TextField(db_column='JobAddres', blank=True, null=True)  # Field name made lowercase.
    jobcity = models.TextField(db_column='JobCity', blank=True, null=True)  # Field name made lowercase.
    jobst = models.TextField(db_column='JobSt', blank=True, null=True)  # Field name made lowercase.
    jobzip = models.TextField(db_column='JobZip', blank=True, null=True)  # Field name made lowercase.
    lender = models.TextField(db_column='LENDER', blank=True, null=True)  # Field name made lowercase.
    gf_field = models.TextField(db_column='GF#', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    jobnotes = models.TextField(db_column='JobNotes', blank=True, null=True)  # Field name made lowercase.
    certify_to = models.TextField(db_column='Certify To', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fname = models.TextField(db_column='Fname', blank=True, null=True)  # Field name made lowercase.
    lname = models.TextField(db_column='Lname', blank=True, null=True)  # Field name made lowercase.
    dear = models.TextField(db_column='Dear', blank=True, null=True)  # Field name made lowercase.
    company = models.TextField(db_column='Company', blank=True, null=True)  # Field name made lowercase.
    client_address1 = models.TextField(db_column='CLIENT_Address1', blank=True, null=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True, null=True)  # Field name made lowercase.
    client_city = models.TextField(db_column='CLIENT_City', blank=True, null=True)  # Field name made lowercase.
    client_address2 = models.TextField(db_column='CLIENT_Address2', blank=True, null=True)  # Field name made lowercase.
    client_state = models.TextField(db_column='CLIENT_State', blank=True, null=True)  # Field name made lowercase.
    client_zip = models.TextField(db_column='CLIENT_Zip', blank=True, null=True)  # Field name made lowercase.
    terms = models.TextField(db_column='Terms', blank=True, null=True)  # Field name made lowercase.
    phone1 = models.TextField(db_column='Phone1', blank=True, null=True)  # Field name made lowercase.
    phone2 = models.TextField(db_column='Phone2', blank=True, null=True)  # Field name made lowercase.
    fax = models.TextField(db_column='Fax', blank=True, null=True)  # Field name made lowercase.
    mobile = models.TextField(db_column='Mobile', blank=True, null=True)  # Field name made lowercase.
    home = models.TextField(db_column='Home', blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='Email', blank=True, null=True)  # Field name made lowercase.
    cnotes = models.TextField(db_column='cNotes', blank=True, null=True)  # Field name made lowercase.
    jobnotes2 = models.TextField(db_column='JobNotes2', blank=True, null=True)  # Field name made lowercase.
    dateneeded = models.TextField(db_column='DateNeeded', blank=True, null=True)  # Field name made lowercase.
    date_notes = models.TextField(db_column='DATE NOTES', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    jobstat = models.TextField(db_column='JobStat', blank=True, null=True)  # Field name made lowercase.
    datecompleted = models.TextField(db_column='DateCompleted', blank=True, null=True)  # Field name made lowercase.
    datepaid = models.TextField(db_column='DatePaid', blank=True, null=True)  # Field name made lowercase.
    job_canceled = models.TextField(db_column='JOB CANCELED', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        # managed = False
        db_table = 'furman_records'


class MasterGeom(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    mtrs = models.CharField(max_length=20, blank=True, null=True)
    meridian = models.CharField(max_length=10, blank=True, null=True)
    township = models.CharField(max_length=10, blank=True, null=True)
    field_range = models.CharField(db_column='_range', max_length=10, blank=True, null=True)  # Field renamed because it started with '_'.
    section = models.CharField(max_length=10, blank=True, null=True)
    t_r = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    anum = models.CharField(max_length=12, blank=True, null=True)
    l1surnam = models.CharField(max_length=32, blank=True, null=True)
    l2block = models.CharField(max_length=10, blank=True, null=True)
    l3surnum = models.CharField(max_length=8, blank=True, null=True)
    duplicat = models.CharField(max_length=1, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    join_type = models.CharField(max_length=50, blank=True, null=True)
    join_field = models.CharField(max_length=200, blank=True, null=True)
    account_nu = models.CharField(max_length=20, blank=True, null=True)
    parcel_num = models.CharField(max_length=10, blank=True, null=True)
    map_number = models.CharField(max_length=20, blank=True, null=True)
    lot_number = models.CharField(max_length=20, blank=True, null=True)
    block_numb = models.CharField(max_length=10, blank=True, null=True)
    subdivisio = models.CharField(max_length=50, blank=True, null=True)
    unit_numbe = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    parcel_cou = models.CharField(max_length=10, blank=True, null=True)
    parcel_typ = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    street_pfx = models.CharField(max_length=2, blank=True, null=True)
    street_sfx = models.CharField(max_length=10, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    globalid = models.CharField(max_length=38, blank=True, null=True)
    edit_date = models.DateField(blank=True, null=True)
    edit_by = models.CharField(max_length=50, blank=True, null=True)
    shape_leng = models.CharField(max_length=255, blank=True, null=True)
    shape_area = models.CharField(max_length=255, blank=True, null=True)
    county_code = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'master_geom'

class Users(AbstractUser):
    # email = models.CharField(max_length=255, blank=True, null=True)
    # password = models.CharField(max_length=255, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Users, self).save(*args, **kwargs)

