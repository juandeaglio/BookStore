import json
import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from Source.Book import Book
from Source.Catalog.PersistentCatalog import PersistentCatalog


def fetchCatalog(request):
    if request.method == "GET":
        catalog = PersistentCatalog()
        catalogContent = catalog.getAllBooksJson()
        return HttpResponse(json.dumps(catalogContent), content_type="application/json")


def loginUser(request):
    if os.environ.get('ENVIRONMENT') == "test" and os.environ.get('TESTPW') and os.environ.get('TESTUSERNAME'):
        if authenticate(request, username=os.environ.get('TESTUSERNAME'), password=os.environ.get('TESTPW')) is None:
            User.objects.create_user(username=os.environ.get('TESTUSERNAME'), password=os.environ.get('TESTPW'))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse(request)
        else:
            return HttpResponse('Unauthorized', status=401)
    return HttpResponse('Not found', status=404)


def addBook(request):
    return None


