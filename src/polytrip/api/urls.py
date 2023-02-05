from django.urls import path

from rest_framework import routers
from rest_framework.authtoken import views

from polytrip.api.views import SchoolViewSet, SiteConfigurationViewSet, TripViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register("trips", TripViewSet, basename="trip")
router.register("schools", SchoolViewSet, basename="school")
router.register("siteconfiguration", SiteConfigurationViewSet, basename="siteconfiguration")

urlpatterns = router.urls

urlpatterns += [path("token-auth/", views.obtain_auth_token)]
