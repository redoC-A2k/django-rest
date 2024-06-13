from home.views import index, person, PersonApi, PersonViewSet, RegisterAPI, LoginAPI
from django.urls import path, include

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'people', PersonViewSet, basename="people")

urlpatterns = [
    path("index/", index), 
    path("person/", person), 
    path("persons/",PersonApi.as_view()),
    path("",include(router.urls)),
    path("register/", RegisterAPI.as_view()),
    path("login/", LoginAPI.as_view())
]
