from django.shortcuts import render

from .models import Crime
from rest_framework import viewsets
from .serializers import CrimeSerializer

# Create your views here.

class CrimeViewSet(viewsets.ModelViewSet):
    queryset = Crime.objects.raw('SELECT * FROM Crime;')
    serializer_class = CrimeSerializer
    
class CrimeInsideViewSet(viewsets.ModelViewSet):
    queryset = Crime.objects.raw("SELECT * FROM Crime where Inside_Outside = 'I'")
    serializer_class = CrimeSerializer
