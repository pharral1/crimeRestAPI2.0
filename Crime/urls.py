from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'crimeinstances', views.CrimeViewSet, "crimeinstances")
router.register(r'crimetypes', views.CrimetypesViewSet, "crimetypes")
#deprecated
#router.register(r'locationdata', views.LocationdataViewSet, "locationdata")
router.register(r'description', views.DescriptionViewSet, "description")
router.register(r'weapon', views.WeaponViewSet, "weapon")
router.register(r'neighborhood', views.NeighborhoodViewSet, "neighborhood")
router.register(r'post', views.PostViewSet, "post")
router.register(r'district', views.DistrictViewSet, "district")
router.register(r'location', views.LocationViewSet, "location")
router.register(r'premise', views.PremiseViewSet, "premise")
router.register(r'location-column-value', views.LocationColumnValueViewSet, "location-column-value")
router.register(r'weapon-count', views.WeaponCountViewSet, "weapon-count")
router.register(r'date-count', views.DateCountViewSet, "date-count")
router.register(r'column-count', views.ColumnCountViewSet, "column-count")

"""
router.register(r'', views.ViewSet, "")
"""
router.register(r'count', views.CountViewSet, "count")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
