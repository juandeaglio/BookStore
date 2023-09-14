from django.urls import path
from . import views
import os
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

urlpatterns = [
    path("fetchCatalog/", views.fetchCatalog),
    path("addBook/", views.addBook),
    path("login/", views.loginUser),
    path("search/", views.searchBooks),
    path("removeBook/", views.removeBook),
    path("createUser/", views.createUser),
    path("csrf/", views.csrf),
]

def createTestCatalogAdminUser():
    if os.environ.get('ENVIRONMENT') == "test" and os.environ.get('TESTPW') and os.environ.get('TESTUSERNAME'):
        if authenticate(None, username=os.environ.get('TESTUSERNAME'),
                        password=os.environ.get('TESTPW')) is None:
            User.objects.create_user(username=os.environ.get('TESTUSERNAME'), password=os.environ.get('TESTPW'))


createTestCatalogAdminUser()
