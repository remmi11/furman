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
    surveyor = models.CharField(max_length=50, blank=True, null=True)
    filed = models.CharField(max_length=50, blank=True, null=True)
    cancelled = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    requested_by = models.CharField(max_length=255, blank=True, null=True)
    well_name = models.CharField(max_length=255, blank=True, null=True)
    well_number = models.CharField(max_length=255, blank=True, null=True)
    join_field = models.CharField(max_length=255, blank=True, null=True)

    aka = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'form_all'


class FormAllFurman(models.Model):
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
    filed = models.CharField(max_length=50, blank=True, null=True)
    cancelled = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    requested_by = models.CharField(max_length=255, blank=True, null=True)
    well_name = models.CharField(max_length=255, blank=True, null=True)
    well_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'form_all_furman'


class FormAllCanadian(models.Model):
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
    filed = models.CharField(max_length=50, blank=True, null=True)
    cancelled = models.CharField(max_length=50, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    requested_by = models.CharField(max_length=255, blank=True, null=True)
    well_name = models.CharField(max_length=255, blank=True, null=True)
    well_number = models.CharField(max_length=255, blank=True, null=True)

    well_name = models.CharField(max_length=255, blank=True, null=True)
    well_number = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'form_all_canadian'


class MasterGeom(models.Model):
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    mtrs = models.CharField(max_length=20, blank=True, null=True)
    meridian = models.CharField(max_length=10, blank=True, null=True)
    township = models.CharField(max_length=10, blank=True, null=True)
    field_range = models.CharField(db_column='_range', max_length=10, blank=True, null=True)  # Field renamed because it started with '_'.
    section = models.CharField(max_length=10, blank=True, null=True)
    t_r = models.CharField(max_length=10, blank=True, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    # anum = models.CharField(max_length=12, blank=True, null=True)
    l1surnam = models.CharField(max_length=32, blank=True, null=True)
    l2block = models.CharField(max_length=10, blank=True, null=True)
    l3surnum = models.CharField(max_length=8, blank=True, null=True)
    # duplicat = models.CharField(max_length=1, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    join_type = models.CharField(max_length=50, blank=True, null=True)
    join_field = models.CharField(max_length=200, blank=True, null=True)
    account_nu = models.CharField(max_length=20, blank=True, null=True)
    # parcel_num = models.CharField(max_length=10, blank=True, null=True)
    map_number = models.CharField(max_length=20, blank=True, null=True)
    lot_number = models.CharField(max_length=20, blank=True, null=True)
    block_numb = models.CharField(max_length=10, blank=True, null=True)
    subdivisio = models.CharField(max_length=50, blank=True, null=True)
    unit_numbe = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    # parcel_cou = models.CharField(max_length=10, blank=True, null=True)
    # parcel_typ = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    street_pfx = models.CharField(max_length=2, blank=True, null=True)
    street_sfx = models.CharField(max_length=10, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    # globalid = models.CharField(max_length=38, blank=True, null=True)
    # edit_date = models.DateField(blank=True, null=True)
    # edit_by = models.CharField(max_length=50, blank=True, null=True)
    # shape_leng = models.CharField(max_length=255, blank=True, null=True)
    # shape_area = models.CharField(max_length=255, blank=True, null=True)
    # county_code = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'master_geom'

class Users(AbstractUser):
    # email = models.CharField(max_length=255, blank=True, null=True)
    # password = models.CharField(max_length=255, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    role_id = models.IntegerField(blank=True, null=True)
    edit_auth = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Users, self).save(*args, **kwargs)
