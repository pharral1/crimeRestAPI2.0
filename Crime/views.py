from django.shortcuts import render

from .models import Crimeinstances
from rest_framework import viewsets
from .serializers import CrimeSerializer
from rest_framework.exceptions import *

# Create your views here.

class CrimeViewSet(viewsets.ModelViewSet):
    #queryset = Crimeinstances.objects.raw('SELECT * FROM CrimeInstances;')
    serializer_class = CrimeSerializer

    def get_queryset(self):

        #prepare queryset object to allow function calls on it but not getting all
        queryset = Crimeinstances.objects

        #if there are no query params, get all, and allow for pagination still
        if not self.request.query_params.keys() or ("page" in self.request.query_params.keys() and len(self.request.query_params.keys()) == 1):
            queryset = Crimeinstances.objects.all().order_by("id")

        #inside outside parsing
        inside_outside = self.request.query_params.get('inside_outside', None)
        
        if inside_outside is not None:
            if inside_outside == "inside":
                queryset = queryset.filter(inside_outside="I").order_by("id")
            elif inside_outside == "outside":
                queryset = queryset.filter(inside_outside="O").order_by("id")
            else:
                return None

        #crime date parsing
        base_date = self.request.query_params.get('crimedate', None)
        if base_date is not None:
            queryset = queryset.filter(crimedate=base_date).order_by("id")

        #date range parsing, splits two dates on a comma delimiter
        date_range = self.request.query_params.get("date_range", None)
        if date_range is not None:
            date_range = date_range.split(",")
            #appending a __range to the crime date value calls a built in range class
            queryset = queryset.filter(crimedate__range=date_range)

        return queryset
    
class CrimeInsideViewSet(viewsets.ModelViewSet):
    queryset = Crimeinstances.objects.raw("select * from CrimeInstances where inside_outside = 'I'")
    serializer_class = CrimeSerializer
