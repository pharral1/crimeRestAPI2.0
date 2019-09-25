from rest_framework import serializers

from .models import Crime

class CrimeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Crime
        fields = ("__all__")
