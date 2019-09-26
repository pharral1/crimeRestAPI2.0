from django.shortcuts import render

from .models import Crimeinstances
from rest_framework import viewsets
from .serializers import CrimeSerializer

# Create your views here.

class CrimeViewSet(viewsets.ModelViewSet):
    queryset = Crimeinstances.objects.raw('SELECT * FROM CrimeInstances;')
    serializer_class = CrimeSerializer
    
class CrimeInsideViewSet(viewsets.ModelViewSet):
    queryset = Crimeinstances.objects.raw("SELECT * FROM CrimeInstances where inside_outside = 'I'")
    serializer_class = CrimeSerializer
