from rest_framework import serializers

from .models import Crimeinstances, Crimetypes

class CrimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("__all__")

class CrimetypesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimetypes
        fields = ("__all__")

class WeaponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("weapon",)

class NeighborhoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("neighborhood",)
class CountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("__all__")
