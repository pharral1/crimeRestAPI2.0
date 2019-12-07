from rest_framework import serializers

from .models import *


class CrimeSerializer(serializers.ModelSerializer):

    #pull in all values from the foreign tables
    description = serializers.CharField(source="crimecode.description", max_length=64)
    location = serializers.CharField(source="locationid.location",max_length=64)
    inside_outside = serializers.CharField(source="locationid.inside_outside",max_length=7)
    post = serializers.CharField(source="locationid.post",max_length=8)
    district = serializers.CharField(source="locationid.district",max_length=64)
    neighborhood = serializers.CharField(source="locationid.neighborhood",max_length=64)
    longitude = serializers.DecimalField(source="locationid.longitude",max_digits=12, decimal_places=10)
    latitude = serializers.DecimalField(source="locationid.latitude",max_digits=12, decimal_places=10)
    premise = serializers.CharField(source="locationid.premise",max_length=48) 
    
    class Meta:
        model = Crimeinstances
        fields = ("crimedate", "crimetime","weapon","total_incidents", "crimecode", "description", "locationid", "location", "inside_outside", "post", "district", "neighborhood", "longitude", "latitude", "premise") 

    #Also an option
    """
    class Meta:
        model = Crimeinstances
        fields = ("__all__")
        depth = 1
    """

class CrimetypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crimetypes
        fields = ("__all__")


class LocationdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("__all__")

#value list serializers
class LocationColumnValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("__all__")

class CrimeColumnValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("__all__")

        
class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("__all__")

class DateCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("crimedate",)
        
class ColumnCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("weapon",)

class LatitudeLongitudeSerializer(serializers.ModelSerializer):
    longitude = serializers.DecimalField(source="locationid.longitude",max_digits=12, decimal_places=10)
    latitude = serializers.DecimalField(source="locationid.latitude",max_digits=12, decimal_places=10)
    class Meta:
        model = Crimeinstances
        fields = ("latitude", "longitude")
        

