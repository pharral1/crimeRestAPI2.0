from rest_framework import serializers

from .models import Crimeinstances

class CrimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crimeinstances
        fields = ("__all__")
