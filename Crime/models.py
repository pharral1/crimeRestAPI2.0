# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Crimeinstances(models.Model):
    crimedate = models.DateField(db_column='crimeDate', blank=True, null=True)  # Field name made lowercase.
    crimetime = models.TimeField(db_column='crimeTime', blank=True, null=True)  # Field name made lowercase.
    crimecode = models.CharField(db_column='crimeCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    weapon = models.CharField(max_length=64, blank=True, null=True)
    total_incidents = models.IntegerField(blank=True, null=True)
    crimeid = models.IntegerField(db_column='crimeId', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CrimeInstances'


class Crimetypes(models.Model):
    crimecode = models.CharField(db_column='crimeCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(max_length=64, blank=True, null=True)
    crimeid = models.IntegerField(db_column='crimeId', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CrimeTypes'


class Inputdata(models.Model):
    crimedate = models.DateField(db_column='crimeDate', blank=True, null=True)  # Field name made lowercase.
    crimetime = models.TimeField(db_column='crimeTime', blank=True, null=True)  # Field name made lowercase.
    crimecode = models.CharField(db_column='crimeCode', max_length=8, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    inside_outside = models.CharField(max_length=7, blank=True, null=True)
    weapon = models.CharField(max_length=64, blank=True, null=True)
    post = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    neighborhood = models.CharField(max_length=64, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    location1 = models.CharField(max_length=48, blank=True, null=True)
    premise = models.CharField(max_length=48, blank=True, null=True)
    vri_name1 = models.CharField(max_length=64, blank=True, null=True)
    total_incidents = models.IntegerField(blank=True, null=True)
    crimeid = models.AutoField(db_column='crimeId', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InputData'


class Locationdata(models.Model):
    location = models.CharField(max_length=64, blank=True, null=True)
    inside_outside = models.CharField(max_length=7, blank=True, null=True)
    post = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=64, blank=True, null=True)
    neighborhood = models.CharField(max_length=64, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    location1 = models.CharField(max_length=48, blank=True, null=True)
    premise = models.CharField(max_length=48, blank=True, null=True)
    vri_name1 = models.CharField(max_length=64, blank=True, null=True)
    crimeid = models.IntegerField(db_column='crimeId', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LocationData'
