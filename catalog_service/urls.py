from django.urls import path
from . import views

urlpatterns = [
    path("fetchCatalog/", views.fetchCatalog)
]
