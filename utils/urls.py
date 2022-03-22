from django.urls import path
from . import views

urlpatterns = [
    path("distance", views.distance),
    path("elevation", views.elevation)
]