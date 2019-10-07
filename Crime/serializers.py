from rest_framework import serializers

from .models import Inputdata, Crimeinstances, Crimetypes

class CrimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inputdata
        fields = ("__all__")

class InputdataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inputdata
        fields = ("__all__")

        
class CrimetypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimetypes
        fields = ("__all__")

class WeaponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inputdata
        fields = ("weapon",)

class NeighborhoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inputdata
        fields = ("neighborhood",)
class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Inputdata
        fields = ("__all__")
