from django.urls import path
from . import views

urlpatterns = [
    path("fetchCatalog/", views.fetchCatalog),
    path("addBook/", views.addBook),
    path("login/", views.loginUser)
]
