from django.shortcuts import render

import json
from rest_framework.schemas import AutoSchema
import coreapi
from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.exceptions import *
from django.db.models.manager import Manager
from rest_framework.response import Response


crime_params_description = {"inside_outside": 'Location, either "inside" or "outside" of a building.',
                            "crimedate": 'Date the crime was committed, must be in YYYY-MM-DD format.',
                            "crimedate__range": "Range of two dates, must be in a FROM,TO format: YYYY-MM-DD,YYYY-MM-DD.",
                            "crimedate__lte": "A date in YYYY-MM-DD format, will return all dates less than or equal to this date.",
                            "crimedate__gte": "A date in YYYY-MM-DD format, will return all dates greater than or equal to this date.",
                            "crimedate__year": "A year in YYYY integer format.",
                            "crimedate__month": "A month in MM integer format.",
                            "crimedate__day": "A day in DD integer format.",
                            "weapon": "A weapon, must be one of the enumerated types.",
                            "location": "A street address, do not include anything after the street.",
                            "latitude": "Latitude, in float format.",
                            "latitude__lte": "Latitude, in float format. Will return all latitudes less or equal to the specified value.",
                            "latitude__gte": "Latitude, in float format. Will return all latitudes greater or equal to the specified value.",
                            "latitude__range": "A range of latitudes in float,float format.",
                            "longitude": "Longitude, in float format.",
                            "longitude__lte": "Longitude, in float format. Will return all longitudes less or equal to the specified value.",
                            "longitude__gte": "Longitude, in float format. Will return all longitudes greater or equal to the specified value.",
                            "longitude__range": "A range of longitudes in float,float format.",
                            "post": "A Police post number, must be an integer",
                            "district": "A Police district string.",
                            "neighborhood": "The neighborhood where the crime took place.",
                            "premise": "The type of premise the crime took place in.",
                            "crimecode": "The code used to describe the crime.",
                            "description": "The description of the crime.",
                            "crimetime": "The time at which the crime occurred in HH:MM:SS format.",
                           }

#generates the AutoSchema used by swagger from a {parameter: description} dictionary (see above)
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
    
    serializer_class = CrimeSerializer
    
    valid_crime_params = ["page",
                          "format",
                          "inside_outside",
                          "crimedate",
                          "crimedate__range",
                          "crimedate__lte",
                          "crimedate__gte",
                          "crimedate__year",
                          "crimedate__month",
                          "crimedate__day",
                          "location",
                          "latitude",
                          "latitude__lte",
                          "latitude__gte",
                          "latitude__range",
                          "longitude",
                          "longitude__lte",
                          "longitude__gte",
                          "longitude__range",
                          "neighborhood",
                          "post",
                          "premise",
                          "district",
                          "weapon",
                          "crimecode",
                          "description",
                          "crimetime",
                          ]

    schema = generate_swagger_schema(crime_params_description)
    
    all_location_params = ["inside_outside",
                           "location",
                           "latitude",
                           "latitude__lte",
                           "latitude__gte",
                           "latitude__range",
                           "longitude",
                           "longitude__lte",
                           "longitude__gte",
                           "longitude__range",
                           "neighborhood",
                           "post",
                           "district",
                           "premise",
                          ]
    
    all_date_params = ["crimedate",
                       "crimedate__range",
                       "crimedate__lte",
                       "crimedate__gte",
                       "crimedate__year",
                       "crimedate__month",
                       "crimedate__day"
                      ]
    main_params = ["weapon",
                   "crimecode",
                   "description",
                   "crimetime",
                   "crimedate"
                  ]

    def get_queryset(self):

        #prepare queryset object to allow function calls on it but not getting all items in dataset
        queryset = Crimeinstances.objects.all()
       
        param_keys = self.request.query_params.keys()

        for key in param_keys:
            if key not in self.valid_crime_params:
                raise ParseError("Bad parameter: %s" % key)
        
        if any(element in self.all_location_params for element in param_keys):
           queryset =  self.parse_location(queryset)

        if any(element in self.all_date_params for element in param_keys):    
            queryset = self.parse_date(queryset)

        #parse the base params using dict based parameter passing
        for key in param_keys:
            if key in self.main_params:
                    value = self.request.query_params.get(key, None)
                    if "range" in key:
                            value = value.split(",")
                    key_val = {key: value}
                    queryset = queryset.filter(**key_val)
                      
        #if query set has not been modified by here, then no filtering has been done,
        #this will be due to bad parameters, so raise a ParseError which returns a 400 bad request
        if isinstance(queryset, Manager):
            raise ParseError("Bad parameters")

        queryset.order_by("id")
        return queryset
    
    def parse_location(self, queryset):
        print(dict(self.request.query_params))
        district = self.request.query_params.get("district", None)
        if district is not None:
            queryset = queryset.filter(locationid__district=district)

        neighborhood = self.request.query_params.get("neighborhood", None)
        if neighborhood is not None:
            queryset = queryset.filter(locationid__neighborhood=neighborhood)

        location = self.request.query_params.get("location", None)
        if location is not None:
            queryset = queryset.filter(locationid__location=location)
                
        premise = self.request.query_params.get("premise", None)
        if premise is not None:
            queryset = queryset.filter(locationid__premise=premise)

        #inside outside parsing
        inside_outside = self.request.query_params.get('inside_outside', None)
        
        if inside_outside is not None and inside_outside not in ["Inside", "Outside"]:
            raise ParseError("Bad parameters, inside_outside must be 'Inside' or 'Outside'")
        elif inside_outside is not None:
            queryset = queryset.filter(locationid__inside_outside=inside_outside)
            
        #USE THIS TO ACCESS FOREIGN TABLE RELATIONSHIPS
        post = self.request.query_params.get('post', None)
        if post is not None:
            queryset = queryset.filter(locationid__post=post)

        latitude = self.request.query_params.get('latitude', None)
        if latitude is not None:
            try:
                latitude = float(latitude)
            except:
                raise ParseError("Bad parameters, latitude must be a float")
        
            queryset = queryset.filter(locationid__latitude=latitude)
        
        #latitude range parsing, split two latitudes on a range
        latitude_range = self.request.query_params.get("latitude__range", None)
        if latitude_range is not None:
            latitude_range = latitude_range.split(",")
                        
            if "" in latitude_range:
                raise ParseError("Bad parameters, latitude__range must provide two floats")
            if len(latitude_range) != 2:
                raise ParseError("Bad parameters, latitude__range must provide two floats")

            try:
                for i in latitude_range:
                    float(i)
            except:
                raise ParseError("Bad parameters, latitude__range must provide two floats")
            queryset = queryset.filter(locationid__latitude__range=latitude_range)
                
        #latitude greater than and less than parsing
        latitude_lte = self.request.query_params.get("latitude__lte", None)
        if latitude_lte is not None:
            try:
                float(latitude_lte)
            except:
                raise ParseError("Bad parameters, latitude must provide a float")
            queryset = queryset.filter(locationid__latitude__lte=latitude_lte)
        
        latitude_gte = self.request.query_params.get("latitude__gte", None)
        if latitude_gte is not None:
            try:
                float(latitude_gte)
            except:
                raise ParseError("Bad parameters, latitude must provide a float")
            queryset = queryset.filter(locationid__latitude__gte=latitude_gte)

        #longitude parsing
        longitude = self.request.query_params.get('longitude', None)
        if longitude is not None:
            try:
                longitude = float(longitude)
            except:
                raise ParseError("Bad parameters, latitude must be a float")
        
            queryset = queryset.filter(locationid__longitude=longitude)
            
        #longitude range parsing, split two longitudes on a range
        longitude_range = self.request.query_params.get("longitude__range", None)
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
            queryset = queryset.filter(locationid__longitude__range=longitude_range)
            
        #longitude greater than and less than parsing
        longitude_lte = self.request.query_params.get("longitude__lte", None)
        if longitude_lte is not None:
            try:
                float(longitude_lte)
            except:
                raise ParseError("Bad parameters, longitude must provide a float")
            queryset = queryset.filter(locationid__longitude__lte=longitude_lte)
            
        longitude_gte = self.request.query_params.get("longitude__gte", None)
        if longitude_gte is not None:
            try:
                float(longitude_gte)
            except:
                raise ParseError("Bad parameters, longitude__gte must provide a float")
            queryset = queryset.filter(locationid__longitude__gte=longitude_gte)
            
        return queryset
    
    def parse_date(self, queryset):
 
        #date range parsing, splits two dates on a comma delimiter
        date_range = self.request.query_params.get("crimedate__range", None)
        if date_range is not None:
            date_range = date_range.split(",")
            if len(date_range) != 2:
                raise ParseError("Bad parameters, date_range must provide date values")
            queryset = queryset.filter(crimedate__range=date_range)

        crimedate = self.request.query_params.get("crimedate", None)
        if crimedate is not None:
            queryset = queryset.filter(crimedate=crimedate)

        date_lte = self.request.query_params.get("crimedate__lte", None)
        if date_lte is not None:
            queryset = queryset.filter(crimedate__lte=date_lte)
            
        date_gte = self.request.query_params.get("crimedate__gte", None)
        if date_gte is not None:
            queryset = queryset.filter(crimedate__gte=date_gte)
        
        return queryset
"""
class WeaponViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WeaponSerializer
    queryset = Inputdata.objects.values("weapon").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        #currently need to cast weapon as char through extra() call as weapon is stored as an ENUM and sort works on an enum index basis in SQL
        return Response(self.queryset.values_list('weapon', flat=True).order_by("weapon").exclude(weapon=""))

    
class NeighborhoodViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NeighborhoodSerializer
    queryset = Locationdata.objects.order_by().values("neighborhood").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('neighborhood', flat=True).order_by("neighborhood").exclude(neighborhood=""))

class CountViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = CountSerializer
    queryset = Inputdata.objects.all()
    
    valid_count_param_keys = ["crimedate",
                              "crimetime",
                              "crimecode",
                              "location",
                              "description",
                              "inside_outside",
                              "weapon",
                              "post",
                              "district",
                              "neighborhood",
                              "longitude",
                              "latitude",
                              "location1",
                              "premise",
                             ]
    def list(self, request, *args, **kwargs):
        search_key = self.request.query_params.keys()

        if len(search_key) > 1:
            raise ParseError("Bad parameters, can only count one at a time")
        elif len(search_key) == 0:
            raise ParseError("Must provide a parameter with a key equal to a column in the crime db and a value equal to a value in that column.")

        search_key = list(self.request.query_params.keys())[0]
        print(search_key)
        if search_key not in self.valid_count_param_keys:
            raise ParseError("Bad parameters, must specify column in database")

        
        
 
        search_value = self.request.query_params[search_key]
        if search_key == "inside_outside":
            if search_value == "inside":
                search_value = "I"
            elif search_value == "outside":
                search_value = "O"
        
        search_filter = {search_key: search_value}
        print(search_filter)
        count = self.queryset.filter(**search_filter).count()
        

        return Response(count)
"""
class CrimetypesViewSet(viewsets.ReadOnlyModelViewSet):

        serializer_class = CrimetypesSerializer
        queryset = Crimetypes.objects.all()


class LocationdataViewSet(viewsets.ReadOnlyModelViewSet):
        serializer_class = LocationdataSerializer
        queryset = Locationdata.objects.all()
