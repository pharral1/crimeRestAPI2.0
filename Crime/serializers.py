from rest_framework import serializers

from .models import Crimeinstances

class CrimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("__all__")

class WeaponSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("weapon",)

class NeighborhoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("neighborhood",)
