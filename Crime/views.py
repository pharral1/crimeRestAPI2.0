#django imports
from django.shortcuts import render
from rest_framework.schemas import AutoSchema
import coreapi
from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.exceptions import *
from django.db.models.manager import Manager
from rest_framework.response import Response
from django.db.models import Count

#python imports
import json
import time
from datetime import datetime

crime_params_description = {"inside_outside": 'Location, either "inside" or "outside" of a building.',
                            "crimedate": 'Date the crime was committed, must be in YYYY-MM-DD format.',
                            "crimedate_range": "Range of two dates, must be in a FROM,TO format: YYYY-MM-DD,YYYY-MM-DD.",
                            "crimedate_lte": "A date in YYYY-MM-DD format, will return all dates less than or equal to this date.",
                            "crimedate_gte": "A date in YYYY-MM-DD format, will return all dates greater than or equal to this date.",
                            "crimedate_year": "A year in YYYY integer format.",
                            "crimedate_month": "A month in MM integer format.",
                            "crimedate_day": "A day in DD integer format.",
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
                            "neighborhood": "The neighborhood where the crime took place.",
                            "premise": "The type of premise the crime took place in.",
                            "crimecode": "The code used to describe the crime.",
                            "description": "The description of the crime.",
                            "crimetime": "The time at which the crime occurred in HH:MM:SS format.",
                            "crimetime_range": "A range of times in HH:MM:SS,HH:MM:SS format.",
                            "crimetime_lte": "A time that will be the upper range for a lte operation in HH:MM:SS foramt.",
                            "crimetime_gte": "A time that will be the lower range for a gte operation in HH:MM:SS foramt.",
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
                          "crimedate_range",
                          "crimedate_lte",
                          "crimedate_gte",
                          "crimedate_year",
                          "crimedate_month",
                          "crimedate_day",
                          "location",
                          "latitude",
                          "latitude_lte",
                          "latitude_gte",
                          "latitude_range",
                          "longitude",
                          "longitude_lte",
                          "longitude_gte",
                          "longitude_range",
                          "neighborhood",
                          "post",
                          "premise",
                          "district",
                          "weapon",
                          "crimecode",
                          "description",
                          "crimetime",
                          "crimetime_range",
                          "crimetime_lte",
                          "crimetime_gte",
                          "column",
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
                           "neighborhood",
                           "post",
                           "district",
                           "premise",
                          ]
    
    all_date_params = ["crimedate",
                       "crimedate_range",
                       "crimedate_lte",
                       "crimedate_gte",
                       "crimedate_year",
                       "crimedate_month",
                       "crimedate_day",
                       "crimetime",
                       "crimetime_range",
                       "crimetime_lte",
                       "crimetime_gte",
                      ]
    main_params = ["weapon",
                   "crimecode",
                   "description",
                  ]

    def get_queryset(self):

        #prepare queryset object to allow function calls on it but not getting all items in dataset
        queryset = Crimeinstances.objects.all().select_related("locationid")
       
        param_keys = self.request.query_params.keys()

        for key in param_keys:
            if key not in self.valid_crime_params:
                raise ParseError("Bad parameter: %s" % key)
        
        if any(element in self.all_location_params for element in param_keys):
           queryset =  self.parse_location(queryset)

        if any(element in self.all_date_params for element in param_keys):    
            queryset = self.parse_datetime(queryset)

        if any(element in self.main_params for element in param_keys):
            queryset = self.parse_details(queryset)
                      
        #if query set has not been modified by here, then no filtering has been done,
        #this will be due to bad parameters, so raise a ParseError which returns a 400 bad request
        if isinstance(queryset, Manager):
            raise ParseError("Bad parameters")

        queryset = queryset.order_by("crimeid")
        return queryset

    def parse_details(self, queryset):

        #weapon parsing
        #split input on comma to find combined fields
        weapon = self.request.query_params.get("weapon", None)
        if weapon is not None:
            if "," in weapon:
                weapon = weapon.split(",")
                queryset = queryset.filter(weapon__in=weapon)
            else:
                queryset = queryset.filter(weapon=weapon)

        crimecode = self.request.query_params.get("crimecode", None)
        if crimecode is not None:
            if "," in crimecode:
                crimecode = crimecode.split(",")
                queryset = queryset.filter(crimecode__in=crimecode)
            else:
                queryset = queryset.filter(crimecode=crimecode)

        description = self.request.query_params.get("description", None)
        if description is not None:
            if "," in description:
                description = description.split(",")
                queryset = queryset.filter(crimecode__description__in=description)
            else:
                queryset = queryset.filter(crimecode__description=description)

        return queryset
    
    def parse_location(self, queryset):
        
        district = self.request.query_params.get("district", None)
        if district is not None:
            if "," in district:
                district = district.split(",")
                queryset = queryset.filter(locationid__district__in=district)
            else:
                queryset = queryset.filter(locationid__district=district)

        neighborhood = self.request.query_params.get("neighborhood", None)
        if neighborhood is not None:
            if "," in neighborhood:
                neighborhood = neighborhood.split(",")
                queryset = queryset.filter(locationid__neighborhood__in=neighborhood)
            else:
                queryset = queryset.filter(locationid__neighborhood=neighborhood)

        location = self.request.query_params.get("location", None)
        if location is not None:
            if "," in location:
                location = location.split(",")
                queryset = queryset.filter(locationid__location__in=location)
            else:
                queryset = queryset.filter(locationid__location=location)
                
        premise = self.request.query_params.get("premise", None)
        if premise is not None:
            if "," in premise:
                premise = premise.split(",")
                queryset = queryset.filter(locationid__premise__in=premise)
            else:
                queryset = queryset.filter(locationid__premise=premise)

        #inside outside parsing
        inside_outside = self.request.query_params.get('inside_outside', None)
        
        if inside_outside is not None and inside_outside not in ["Inside", "Outside"]:
            raise ParseError("Bad parameters, inside_outside must be 'Inside' or 'Outside'")
        elif inside_outside is not None:
            queryset = queryset.filter(locationid__inside_outside=inside_outside)
            
        #post number parsing
        post = self.request.query_params.get('post', None)
        if post is not None:
            if "," in post:
                post = post.split(",")
                queryset = queryset.filter(locationid__post__in=post)
            else:
                queryset = queryset.filter(locationid__post=post)

        #latitude parsing
        latitude = self.request.query_params.get('latitude', None)
        if latitude is not None:
            try:
                latitude = float(latitude)
            except:
                raise ParseError("Bad parameters, latitude must be a float")
        
            queryset = queryset.filter(locationid__latitude=latitude)
        
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
            queryset = queryset.filter(locationid__latitude__range=latitude_range)
                
        #latitude greater than and less than parsing
        latitude_lte = self.request.query_params.get("latitude_lte", None)
        if latitude_lte is not None:
            try:
                float(latitude_lte)
            except:
                raise ParseError("Bad parameters, latitude_lte must provide a float")
            queryset = queryset.filter(locationid__latitude__lte=latitude_lte)
        
        latitude_gte = self.request.query_params.get("latitude_gte", None)
        if latitude_gte is not None:
            try:
                float(latitude_gte)
            except:
                raise ParseError("Bad parameters, latitude_gte must provide a float")
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
            queryset = queryset.filter(locationid__longitude__range=longitude_range)
            
        #longitude greater than and less than parsing
        longitude_lte = self.request.query_params.get("longitude_lte", None)
        if longitude_lte is not None:
            try:
                float(longitude_lte)
            except:
                raise ParseError("Bad parameters, longitude_lte must provide a float")
            queryset = queryset.filter(locationid__longitude__lte=longitude_lte)
            
        longitude_gte = self.request.query_params.get("longitude_gte", None)
        if longitude_gte is not None:
            try:
                float(longitude_gte)
            except:
                raise ParseError("Bad parameters, longitude_gte must provide a float")
            queryset = queryset.filter(locationid__longitude__gte=longitude_gte)
            
        return queryset
    
    def parse_datetime(self, queryset):
 
        #date range parsing, splits two dates on a comma delimiter
        date_range = self.request.query_params.get("crimedate_range", None)
        if date_range is not None:
            date_range = date_range.split(",")
            if len(date_range) != 2:
                raise ParseError("Bad parameters, crimedate_range must provide date values")
            self.validate_date(date_range[0])
            self.validate_date(date_range[1])
            queryset = queryset.filter(crimedate__range=date_range)

        #date value pasrsing
        crimedate = self.request.query_params.get("crimedate", None)
        if crimedate is not None:
            if "," in crimedate:
                crimedate = crimedate.split(",")
                for date in crimedate:
                    self.validate_date(date)
                queryset = queryset.filter(crimedate__in=crimedate)
            else:
                self.validate_date(crimedate)
                queryset = queryset.filter(crimedate=crimedate)

        crimedate_year = self.request.query_params.get("crimedate_year", None)
        if crimedate_year is not None:
            if "," in crimedate_year:
                crimedate_year = crimedate_year.split(",")
                for year in crimedate_year:
                    try:
                        int(year)
                    except:
                        raise ParseError("Year must be an integer")
                queryset = queryset.filter(crimedate__year__in=crimedate_year)
            else:
                try:
                    int(crimedate_year)
                except:
                    raise ParseError("Year must be an integer")
                queryset = queryset.filter(crimedate__year=crimedate_year)

        crimedate_month = self.request.query_params.get("crimedate_month", None)
        if crimedate_month is not None:
            if "," in crimedate_month:
                crimedate_month = crimedate_month.split(",")
                for month in crimedate_month:
                    try:
                        int(month)
                    except:
                        raise ParseError("Month must be an integer")
                queryset = queryset.filter(crimedate__month__in=crimedate_month)
            else:
                try:
                    int(crimedate_month)
                except:
                    raise ParseError("Month must be an integer")
                queryset = queryset.filter(crimedate__month=crimedate_month)

        crimedate_day = self.request.query_params.get("crimedate_day", None)
        if crimedate_day is not None:
            if "," in crimedate_day:
                crimedate_day = crimedate_day.split(",")
                for day in crimedate_day:
                    try:
                        int(day)
                    except:
                        raise ParseError("Day must be an integer")
                queryset = queryset.filter(crimedate__day__in=crimedate_day)
            else:
                try:
                    int(crimedate_day)
                except:
                    raise ParseError("Day must be an integer")
                queryset = queryset.filter(crimedate__day=crimedate_day)

        #date range parsing
        date_lte = self.request.query_params.get("crimedate_lte", None)
        if date_lte is not None:
            self.validate_date(date_lte)
            queryset = queryset.filter(crimedate__lte=date_lte)
            
        date_gte = self.request.query_params.get("crimedate_gte", None)
        if date_gte is not None:
            self.validate_date(date_gte)
            queryset = queryset.filter(crimedate__gte=date_gte)

        crimetime = self.request.query_params.get("crimetime", None)
        if crimetime is not None:
            if "," in crimetime:
                crimetime = crimetime.split(",")
                for t in crimetime:
                    self.validate_time(t)
                queryset = queryset.filter(crimetime__in=crimetime)
            else:
                self.validate_time(crimetime)
                queryset = queryset.filter(crimetime=crimetime)
        
        crimetime_range = self.request.query_params.get("crimetime_range", None)
        if crimetime_range is not None:
            crimetime_range = crimetime_range.split(",")
            if len(crimetime_range) != 2:
                raise ParseError("Bad parameters, crimetime_range must provide two date values")
            self.validate_time(crimetime_range[0])
            self.validate_time(crimetime_range[1])
            queryset = queryset.filter(crimetime__range=crimetime_range)

        crimetime_lte = self.request.query_params.get("crimetime_lte", None)
        if crimetime_lte is not None:
            self.validate_time(crimetime_lte)
            queryset = queryset.filter(crimetime__lte=crimetime_lte)

        crimetime_gte = self.request.query_params.get("crimetime_gte", None)
        if crimetime_gte is not None:
            self.validate_time(crimetime_gte)
            queryset = queryset.filter(crimetime__gte=crimetime_gte)
            
        return queryset

    def validate_date(self, date_val):
        try:
            form = datetime.strptime(date_val, "%Y-%m-%d")
        except:
            raise ParseError("Invalid date value, must be in YYYY-MM-DD format")
            
    def validate_time(self, time_val):
        try:
            form = time.strptime(time_val, "%H:%M:%S")
        except:
            raise ParseError("Invalid time format, time must be in HH:MM:SS format")

class DescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DescriptionSerializer
    queryset = Crimetypes.objects.order_by().values("description").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('description', flat=True).order_by("description").exclude(description="").exclude(description=None))

class WeaponViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WeaponSerializer
    queryset = Crimeinstances.objects.values("weapon").distinct()

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
        return Response(self.queryset.values_list('neighborhood', flat=True).order_by("neighborhood").exclude(neighborhood="").exclude(neighborhood=None))


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    queryset = Locationdata.objects.order_by().values("post").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('post', flat=True).order_by("post").exclude(post="").exclude(post=None))

class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DistrictSerializer
    queryset = Locationdata.objects.order_by().values("district").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('district', flat=True).order_by("district").exclude(district="").exclude(district=None))


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LocationSerializer
    queryset = Locationdata.objects.order_by().values("location").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('location', flat=True).order_by("location").exclude(location="").exclude(location=None))

class PremiseViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PremiseSerializer
    queryset = Locationdata.objects.order_by().values("premise").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('premise', flat=True).order_by("premise").exclude(premise="").exclude(premise=None))
"""
class ViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = Serializer
    queryset = Locationdata.objects.order_by().values("").distinct()

    #to return all distinct values of the queryset, must override the list method and call values_list on the queryset
    def list(self, request, *args, **kwargs):
        #original example has the following, but the below works just as well without the second filter call
        #query set = self.filter_queryset(self.get_queryset())

        #return a flat list of distinct values without the empty string
        return Response(self.queryset.values_list('', flat=True).order_by("").exclude(="").exclude(=None))

"""


class CountViewSet(CrimeViewSet):

        serializer_class = CountSerializer

        def list(self, request, *args, **kwargs):
            queryset = super().get_queryset()
            count = queryset.count()
            return Response(count)
            

class CrimetypesViewSet(viewsets.ReadOnlyModelViewSet):

        serializer_class = CrimetypesSerializer
        queryset = Crimetypes.objects.all()


class LocationdataViewSet(viewsets.ReadOnlyModelViewSet):
        serializer_class = LocationdataSerializer
        queryset = Locationdata.objects.all()

class WeaponCountViewSet(CrimeViewSet):
        serializer_class = WeaponCountSerializer
        
        def list(self, request, *args, **kwargs):
            param_keys = self.request.query_params.keys()
            
            
            if len(param_keys) == 0:
                queryset = Crimeinstances.objects.all().values("weapon").annotate(total=Count("weapon")).order_by("total")
                flatten = {}
                for val in queryset:
                    flatten[val["weapon"]] = val["total"]
                return Response(flatten)

            else:
                queryset = super().get_queryset()
                queryset = queryset.values("weapon").annotate(total=Count("weapon")).order_by("total")
                flatten = {}
                for val in queryset:
                    flatten[val["weapon"]] = val["total"]
                return Response(flatten)

class DateCountViewSet(CrimeViewSet):
        serializer_class = WeaponCountSerializer
        
        def list(self, request, *args, **kwargs):
            param_keys = self.request.query_params.keys()
            
            
            if len(param_keys) == 0:
                queryset = Crimeinstances.objects.all().values("crimedate__year", "crimedate__month").annotate(total=Count("pk")).order_by("crimedate")

                flatten = {}
                for val in queryset:
                    if val["crimedate__year"] not in flatten.keys():
                        flatten[val["crimedate__year"]] = {}
                        flatten[val["crimedate__year"]][val["crimedate__month"]] = val["total"]
                    else:
                        if val["crimedate__month"] not in flatten[val["crimedate__year"]].keys():
                            flatten[val["crimedate__year"]][val["crimedate__month"]] = val["total"]
                        else:
                            flatten[val["crimedate__year"]][val["crimedate__month"]] += val["total"]
                return Response(flatten)
            else:
                queryset = super().get_queryset()
                queryset = queryset.values("weapon").values("crimedate__year", "crimedate__month").annotate(total=Count("pk")).order_by("crimedate")
                flatten = {}
                for val in queryset:
                    if val["crimedate__year"] not in flatten.keys():
                        flatten[val["crimedate__year"]] = {}
                        flatten[val["crimedate__year"]][val["crimedate__month"]] = val["total"]
                    else:
                        if val["crimedate__month"] not in flatten[val["crimedate__year"]].keys():
                            flatten[val["crimedate__year"]][val["crimedate__month"]] = val["total"]
                        else:
                            flatten[val["crimedate__year"]][val["crimedate__month"]] += val["total"]
                return Response(flatten)        

class ColumnCountViewSet(CrimeViewSet):
        serializer_class = ColumnCountSerializer
        this_crime_params = crime_params_description
        this_crime_params["column"] = "The column to count values for"
        schema = generate_swagger_schema(this_crime_params)
        valid_columns = ["weapon", "crimecode", "crimetime"]
        
        def list(self, request, *args, **kwargs):
            param_keys = self.request.query_params.keys()
            if "column" not in param_keys:
                    raise ParseError("Column is a required query parameter")

            column = self.request.query_params.get("column")
            if column not in self.valid_columns:
                    raise ParseError("Passed column not valid")
            
            if len(param_keys) == 1:
                queryset = Crimeinstances.objects.all().values(column).annotate(total=Count(column)).order_by("total")
                flatten = {}
                for val in queryset:
                    if column == "crimetime":
                        flatten[str(val[column])] = val["total"]
                    else:
                        flatten[val[column]] = val["total"]
                print(flatten)
                return Response(flatten)

            else:
                queryset = super().get_queryset()
                queryset = queryset.values(column).annotate(total=Count(column)).order_by("total")
                flatten = {}
                for val in queryset:
                    if column == "crimetime":
                        flatten[str(val[column])] = val["total"]
                    else:
                        flatten[val[column]] = val["total"]
                return Response(flatten)
