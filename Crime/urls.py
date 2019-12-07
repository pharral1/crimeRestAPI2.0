from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'crimeinstances', views.CrimeViewSet, "crimeinstances")
router.register(r'crimetypes', views.CrimetypesViewSet, "crimetypes")
router.register(r'locationdata', views.LocationdataViewSet, "locationdata")
router.register(r'crime-column-value', views.CrimeColumnValueViewSet, "crime-column-value")
router.register(r'location-column-value', views.LocationColumnValueViewSet, "location-column-value")
router.register(r'date-count', views.DateCountViewSet, "date-count")
router.register(r'column-count', views.ColumnCountViewSet, "column-count")
router.register(r'latitude-longitude', views.LatitudeLongitudeViewSet, "latitude-longitude")
"""
router.register(r'', views.ViewSet, "")
"""
router.register(r'count', views.CountViewSet, "count")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
