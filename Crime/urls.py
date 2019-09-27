from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'crimeinstances', views.CrimeViewSet, "crimeinstances")
router.register(r'weapons', views.WeaponViewSet, "weapons")
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
]
