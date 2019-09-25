from django.db import models

# Create your models here.

class CrimeModel(models.Model):
    class Meta:
        managed = False
        db_table = "crimes"
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Crime(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    crimedate = models.DateField(db_column='CrimeDate', blank=True, null=True)  # Field name made lowercase.
    crimetime = models.TimeField(db_column='CrimeTime', blank=True, null=True)  # Field name made lowercase.
    crimecode = models.CharField(db_column='CrimeCode', max_length=64, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=64, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=64, blank=True, null=True)  # Field name made lowercase.
    inside_outside = models.CharField(db_column='Inside_Outside', max_length=64, blank=True, null=True)  # Field name made lowercase.
    weapon = models.CharField(db_column='Weapon', max_length=64, blank=True, null=True)  # Field name made lowercase.
    post = models.IntegerField(db_column='Post', blank=True, null=True)  # Field name made lowercase.
    district = models.CharField(db_column='District', max_length=64, blank=True, null=True)  # Field name made lowercase.
    neighborhood = models.CharField(db_column='Neighborhood', max_length=64, blank=True, null=True)  # Field name made lowercase.
    longitude = models.DecimalField(db_column='Longitude', max_digits=11, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    latitude = models.DecimalField(db_column='Latitude', max_digits=11, decimal_places=8, blank=True, null=True)  # Field name made lowercase.
    location1 = models.CharField(db_column='Location1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    premise = models.CharField(db_column='Premise', max_length=64, blank=True, null=True)  # Field name made lowercase.
    vri_name1 = models.CharField(max_length=64, blank=True, null=True)
    total_incidents = models.IntegerField(db_column='Total_Incidents', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Crime'
