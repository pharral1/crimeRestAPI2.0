from rest_framework import serializers

from .models import *


class CrimeSerializer(serializers.HyperlinkedModelSerializer):
    """
    class Meta:
        model = Crimeinstances
        fields = ("__all__")
    """
    inside_outside = serializers.CharField(source="locationid.inside_outside")
    longitude = serializers.CharField(source="locationid.longitude")
    
    class Meta:
        model = Crimeinstances
        fields = ("crimedate", "crimetime","weapon","total_incidents", "crimecode", "locationid", "inside_outside", "longitude")
    
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
