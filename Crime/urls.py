from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'inputdata', views.InputdataViewSet, "inputdata")
#router.register(r'crimeinstances', views.CrimeViewSet, "crimeinstances")
router.register(r'crimetypes', views.CrimetypesViewSet, "crimetypes")
router.register(r'weapons', views.WeaponViewSet, "weapons")
router.register(r'neighborhoods', views.NeighborhoodViewSet, "neighborhoods")
router.register(r'count', views.CountViewSet, "count")
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
