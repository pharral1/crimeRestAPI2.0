from django.shortcuts import render

from rest_framework.schemas import AutoSchema
import coreapi
from .models import Crimeinstances
from rest_framework import viewsets
from .serializers import CrimeSerializer, WeaponSerializer, NeighborhoodSerializer
from rest_framework.exceptions import *
from django.db.models.manager import Manager
from rest_framework.response import Response

crime_params_description = {"inside_outside": 'Location, either "inside" or "outside" of a building.',
                            "crime_date": 'Date the crime was committed, must be in YYYY-MM-DD format.',
                            "date_range": "Range of two dates, must be in a FROM,TO format: YYYY-MM-DD,YYYY-MM-DD.",
                            "date_lte": "A date in YYYY-MM-DD format, will return all dates less than or equal to this date.",
                            "date_gte": "A date in YYYY-MM-DD format, will return all dates greater than or equal to this date.",
                            "year": "A year in YYYY integer format.",
                            "month": "A month in MM integer format.",
                            "day": "A day in DD integer format.",
                            "weapon": "A weapon, must be one of the enumerated types.",
                            "location": "A street address, do not include anything after the street.",
                            "latitude": "Latitude, in float format.",
                            "latitude_lte": "Latitude, in float format. Will return all latitudes less or equal to the specified value.",
                            "latitude_gte": "Latitude, in float format. Will return all latitudes greater or equal to the specified value.",
                            "latitude_range": "A range of latitudes in float,float format.",
                            "longitude": "Longitude, in float format.",
                            "longitude_lte": "Longitude, in float format. Will return all longitudes less or equal to the specified value.",
                            "longitude_gte": "Longitude, in float format. Will return all longitudes greater or equal to the specified value.",
                            "longitude_range": "A range of longitudes in float,float format.",
                            "post": "A Police post number, must be an integer",
                            "district": "A Police district string.",
                           }

def generate_swagger_schema(description_dict):
        manual_fields = []
        for field_name in description_dict:
            field = coreapi.Field(field_name,
                                  required=False,
                                  location='query',
                                  description=description_dict[field_name]
                                 )
            manual_fields.append(field)
        return AutoSchema(manual_fields=manual_fields)


class CrimeViewSet(viewsets.ReadOnlyModelViewSet):
    #queryset = Crimeinstances.objects.raw('SELECT * FROM CrimeInstances;')
    serializer_class = CrimeSerializer
    
    valid_crime_params = ["page",
                          "format",
                          "inside_outside",
                          "crimedate",
                          "date_range",
                          "date_lte",
                          "date_gte",
                          "year",
                          "month",
                          "day",
                          "weapon",
                          "location",
                          "latitude",
                          "latitude_lte",
                          "latitude_gte",
                          "latitude_range",
                          "longitude",
                          "longitude_lte",
                          "longitude_gte",
                          "longitude_range",
                          "post",
                          "district",
                          ]

    schema = generate_swagger_schema(crime_params_description)
    
    all_location_params = ["inside_outside",
                           "location",
                           "latitude",
                           "latitude_lte",
                           "latitude_gte",
                           "latitude_range",
                           "longitude",
                           "longitude_lte",
                           "longitude_gte",
                           "longitude_range",
                           "post",
                           "district",
                          ]
    all_date_params = ["crimedate",
                       "date_range",
                       "date_lte",
                       "date_gte",
                       "year",
                       "month",
                       "day"
                      ]
    

    def get_queryset(self):

        #prepare queryset object to allow function calls on it but not getting all items in dataset
        queryset = Crimeinstances.objects
        #queryset = Crimeinstances.objects.all()

        param_keys = self.request.query_params.keys()

        for key in param_keys:
            if key not in self.valid_crime_params:
                raise ParseError("Bad parameter: %s" % key)

        #if there are no query params and/or there are no query parameters
        #plus a page number or format type, get all, and allow for pagination or formatting still
        if not self.request.query_params.keys() or \
           ("page" in self.request.query_params.keys() and len(self.request.query_params.keys()) == 1) or \
           ("format" in self.request.query_params.keys() and len(self.request.query_params.keys()) == 1) or \
           ("page" in self.request.query_params.keys() and "format" in self.request.query_params.keys() and len(self.request.query_params.keys()) == 2):
        
            queryset = Crimeinstances.objects.all()


            
        if any(element in self.all_location_params for element in param_keys):
            queryset = self.parse_location(queryset)

        if any(element in self.all_date_params for element in param_keys):    
            queryset = self.parse_date(queryset)

        queryset = self.parse_details(queryset)
        
        #if query set has not been modified by here, then no filtering has been done,
        #this will be due to bad parameters, so raise a ParseError which returns a 400 bad request
        if isinstance(queryset, Manager):
            raise ParseError("Bad parameters")

        queryset.order_by("id")
        return queryset
    
    def parse_location(self, queryset):
        print("Found location parameter")

        #inside outside parsing
        inside_outside = self.request.query_params.get('inside_outside', None)
        
        if inside_outside is not None:
            if inside_outside == "inside":
                queryset = queryset.filter(inside_outside="I")
            elif inside_outside == "outside":
                queryset = queryset.filter(inside_outside="O")
            else:
                raise ParseError("Bad parameters, inside_outside must be 'inside' or 'outside'")

        #post parsing    
        post = self.request.query_params.get("post", None)
        if post is not None:
            try:
                int(post)
            except:
                raise ParseError("Bad parameters, post must be an int")
            queryset = queryset.filter(post=post)

        #location parsing
        #locations will contain spaces within them, these can be encoded in the url as %20 or the + character (latter is unsafe)
        #eg: <url>?location=4300%20DAVIS%20AVE OR <url>?location=4300+DAVIS+AVE
        location = self.request.query_params.get("location", None)
        if location is not None:
            queryset = queryset.filter(location=location)

        #latitude parsing
        latitude = self.request.query_params.get("latitude", None)
        if latitude is not None:
            queryset = queryset.filter(latitude=latitude)

        #latitude range parsing, split two latitudes on a range
        latitude_range = self.request.query_params.get("latitude_range", None)
        if latitude_range is not None:
            latitude_range = latitude_range.split(",")
                        
            if "" in latitude_range:
                raise ParseError("Bad parameters, latitude_range must provide two floats")
            if len(latitude_range) != 2:
                raise ParseError("Bad parameters, latitude_range must provide two floats")

            try:
                for i in latitude_range:
                    float(i)
            except:
                raise ParseError("Bad parameters, latitude_range must provide two floats")
            
            #appending a __range to the crime date value calls a built in range class
            queryset = queryset.filter(latitude__range=latitude_range)

        #latitude greater than and less than parsing
        latitude_lte = self.request.query_params.get("latitude_lte", None)
        if latitude_lte is not None:
            try:
                float(latitude_lte)
            except:
                raise ParseError("Bad parameters, latitude must provide a float")
            queryset = queryset.filter(latitude__lte=latitude_lte)

        latitude_gte = self.request.query_params.get("latitude_gte", None)
        if latitude_gte is not None:
            try:
                float(latitude_gte)
            except:
                raise ParseError("Bad parameters, latitude must provide a float")
            queryset = queryset.filter(latitude__gte=latitude_gte)

        #longitude parsing
        longitude = self.request.query_params.get("longitude", None)
        if longitude is not None:
            queryset = queryset.filter(longitude=longitude)

        #longitude range parsing, split two longitudes on a range
        longitude_range = self.request.query_params.get("longitude_range", None)
        if longitude_range is not None:
            longitude_range = longitude_range.split(",")
                        
            if "" in longitude_range:
                raise ParseError("Bad parameters, longitude_range must provide two floats")
            if len(longitude_range) != 2:
                raise ParseError("Bad parameters, longitude_range must provide two floats")

            try:
                for i in longitude_range:
                    float(i)
            except:
                raise ParseError("Bad parameters, longitude_range must provide two floats")
            
            #appending a __range to the crime date value calls a built in range class
            queryset = queryset.filter(longitude__range=longitude_range)

        #longitude greater than and less than parsing
        longitude_lte = self.request.query_params.get("longitude_lte", None)
        if longitude_lte is not None:
            try:
                float(longitude_lte)
            except:
                raise ParseError("Bad parameters, longitude must provide a float")
            queryset = queryset.filter(longitude__lte=longitude_lte)

        longitude_gte = self.request.query_params.get("longitude_gte", None)
        if longitude_gte is not None:
            try:
                float(longitude_gte)
            except:
                raise ParseError("Bad parameters, longitude_gte must provide a float")
            queryset = queryset.filter(longitude__gte=longitude_gte)

        #district parsing
        district = self.request.query_params.get("district", None)
        if district is not None:
            queryset = queryset.filter(district=district)
            
        return queryset
    
    def parse_date(self, queryset):
        print("Found date parameter")
        #crime date parsing
        base_date = self.request.query_params.get('crimedate', None)
        if base_date is not None:
            queryset = queryset.filter(crimedate=base_date) 

        #date range parsing, splits two dates on a comma delimiter
        date_range = self.request.query_params.get("date_range", None)
        if date_range is not None:
            date_range = date_range.split(",")
            if len(date_range) != 2:
                raise ParseError("Bad parameters, date_range must provide date values")
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

        return queryset

    def parse_details(self, queryset):
        
        #weapon parsing
        weapon = self.request.query_params.get("weapon", None)
        if weapon is not None:
            queryset = queryset.filter(weapon=weapon)

        return queryset

class WeaponViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WeaponSerializer
    queryset = Crimeinstances.objects.values("weapon").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        #currently need to cast weapon as char through extra() call as weapon is stored as an ENUM and sort works on an enum index basis in SQL
        return Response(self.queryset.values_list('weapon', flat=True).extra(select={'weapon': "CAST(weapon AS CHAR)"}).order_by("weapon").exclude(weapon=""))

    
class NeighborhoodViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NeighborhoodSerializer
    queryset = Crimeinstances.objects.order_by().values("neighborhood").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('neighborhood', flat=True).order_by("neighborhood").exclude(neighborhood=""))

