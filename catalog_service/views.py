import json
import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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
    createTestCatalogAdminUser(request)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        return attemptLogin(password, request, username)

    return HttpResponse('Not found', status=404)


def attemptLogin(password, request, username):
    try:
        loginWithCredentials(request, username, password)
        return HttpResponse(request)

    except ValueError as loginFailed:
        return HttpResponse('Unauthorized', status=401)


def loginWithCredentials(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    else:
        raise(ValueError("Unauthorized"))


def createTestCatalogAdminUser(request):
    if os.environ.get('ENVIRONMENT') == "test" and os.environ.get('TESTPW') and os.environ.get('TESTUSERNAME'):
        if authenticate(request, username=os.environ.get('TESTUSERNAME'), password=os.environ.get('TESTPW')) is None:
            User.objects.create_user(username=os.environ.get('TESTUSERNAME'), password=os.environ.get('TESTPW'))


@login_required
def addBook(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        releaseYear = request.POST.get("releaseYear")
        catalog = PersistentCatalog()
        catalog.add([Book(title=title, author=author, releaseYear=releaseYear)])
        return HttpResponse(status=200)
    return HttpResponse("Not found", status=404)

