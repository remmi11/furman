from django.db import models

# Create your models here.

class Tickets(models.Model):
    subject = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=1)
    survey_type = models.CharField(max_length=50, blank=True, null=True)

    county = models.CharField(max_length=50, blank=True, null=True)
    subdivision = models.CharField(max_length=50, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    sub_block = models.CharField(max_length=10, blank=True, null=True)
    lot = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=255, blank=True, null=True)

    survey = models.CharField(max_length=32, blank=True, null=True)
    rural_block = models.CharField(max_length=10, blank=True, null=True)
    rural_section = models.CharField(max_length=8, blank=True, null=True)
    
    meridian = models.CharField(max_length=10, blank=True, null=True)
    t_r = models.CharField(max_length=10, blank=True, null=True)
    plss_section = models.CharField(db_column='_range', max_length=10, blank=True, null=True)  # Field renamed because it started with '_'.
    
    description = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        # managed = False
        db_table = 'tickets'