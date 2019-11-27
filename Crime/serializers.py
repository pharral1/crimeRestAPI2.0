from rest_framework import serializers

from .models import *


class CrimeSerializer(serializers.HyperlinkedModelSerializer):
    """
    class Meta:
        model = Crimeinstances
        fields = ("__all__")
    """
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
        fields = ("crimedate", "crimetime","weapon","total_incidents", "crimecode", "locationid", "location", "inside_outside", "post", "district", "neighborhood", "longitude", "latitude", "premise")
    
class CrimetypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimetypes
        fields = ("__all__")


class LocationdataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("__all__")

#value list serializers
class DescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimetypes
        fields = ("description")

class WeaponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("weapon",)

class NeighborhoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("neighborhood",)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("post",)

class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("district",)

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("location",)

class PremiseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Locationdata
        fields = ("premise",)

class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("__all__")

class WeaponCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("weapon",)

class DateCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("crimedate",)
        
class ColumnCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("weapon",)
