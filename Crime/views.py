from django.shortcuts import render

from .models import Crimeinstances
from rest_framework import viewsets
from .serializers import CrimeSerializer, WeaponSerializer, NeighborhoodSerializer
from rest_framework.exceptions import *
from django.db.models.manager import Manager
from rest_framework.response import Response
# Create your views here.

class CrimeViewSet(viewsets.ModelViewSet):
    #queryset = Crimeinstances.objects.raw('SELECT * FROM CrimeInstances;')
    serializer_class = CrimeSerializer
    valid_crime_params = ["page",
                          "inside_outside",
                          "crimedate",
                          "date_range",
                          "date_lte",
                          "date_gte",
                          "year",
                          "month",
                          "day",
                          "weapon"]
    

    def get_queryset(self):

        #prepare queryset object to allow function calls on it but not getting all
        queryset = Crimeinstances.objects

        param_keys = self.request.query_params.keys()

        for key in param_keys:
            if key not in self.valid_crime_params:
                raise ParseError("Bad parameter: %s" % key)

        #if there are no query params and/or there are no query parameters
        #plus a page number, get all, and allow for pagination still
        if not self.request.query_params.keys() or \
           ("page" in self.request.query_params.keys() and len(self.request.query_params.keys()) == 1):
        
            queryset = Crimeinstances.objects.all()

        #inside outside parsing
        inside_outside = self.request.query_params.get('inside_outside', None)
        
        if inside_outside is not None:
            if inside_outside == "inside":
                queryset = queryset.filter(inside_outside="I")
            elif inside_outside == "outside":
                queryset = queryset.filter(inside_outside="O")
            else:
                return None

        #crime date parsing
        base_date = self.request.query_params.get('crimedate', None)
        if base_date is not None:
            queryset = queryset.filter(crimedate=base_date) 

        #date range parsing, splits two dates on a comma delimiter
        date_range = self.request.query_params.get("date_range", None)
        if date_range is not None:
            date_range = date_range.split(",")
            #appending a __range to the crime date value calls a built in range class
            queryset = queryset.filter(crimedate__range=date_range)

        date_lte = self.request.query_params.get("date_lte", None)
        if date_lte is not None:
            queryset = queryset.filter(crimedate__lte=date_lte)

        date_gte = self.request.query_params.get("date_gte", None)
        if date_gte is not None:
            queryset = queryset.filter(crimedate__gte=date_gte)

        #year parsing
        year = self.request.query_params.get("year", None)
        if year is not None:
            try:
                year = int(year)
            except:
                raise ParseError("Bad parameters, year must be int")
            queryset = queryset.filter(crimedate__year=year)

        #month parsing
        month = self.request.query_params.get("month", None)
        if month is not None:
            try:
                month = int(month)
            except:
                raise ParseError("Bad parameters, month must be int")
            queryset = queryset.filter(crimedate__month=month)

        #day parsing
        day = self.request.query_params.get("day", None)
        if day is not None:
            try:
                day = int(day)
            except:
                raise ParseError("Bad parameters, day must be int")
            queryset = queryset.filter(crimedate__day=day)

        #weapon parsing
        weapon = self.request.query_params.get("weapon", None)
        if weapon is not None:
            queryset = queryset.filter(weapon=weapon)
        
        

        #if query set has not been modified by here, then no filtering has been done,
        #this will be due to bad parameters, so raise a ParseError which returns a 400 bad request
        if isinstance(queryset, Manager):
            raise ParseError("Bad parameters")

        queryset.order_by("id")
        return queryset

class WeaponViewSet(viewsets.ModelViewSet):
    serializer_class = WeaponSerializer
    queryset = Crimeinstances.objects.order_by().values("weapon").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct weapons without the empty string
        return Response(self.queryset.values_list('weapon', flat=True).exclude(weapon=""))

    
class NeighborhoodViewSet(viewsets.ModelViewSet):
    serializer_class = NeighborhoodSerializer
    queryset = Crimeinstances.objects.order_by().values("neighborhood").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct weapons without the empty string
        return Response(self.queryset.values_list('neighborhood', flat=True).order_by("neighborhood").exclude(neighborhood=""))

