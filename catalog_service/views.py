import json
import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from Source.Book import Book
from Source.Catalog.PersistentCatalog import PersistentCatalog


def fetchCatalog(request):
    if request.method == "GET":
        catalog = PersistentCatalog()
        catalogContent = catalog.getAllBooksJson()
        response = HttpResponse(json.dumps(catalogContent), content_type="application/json")
        print(response.headers)
        return response


def searchBooks(request):
    if request.method == "GET":
        title = request.GET.get("title")
        catalog = PersistentCatalog()
        books = catalog.search(title)
        jsonArray = []
        for book in books:
            jsonArray.append(book.to_json())

        return HttpResponse(json.dumps(jsonArray), content_type="application/json")


def loginUser(request):
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
        raise (ValueError("Unauthorized"))


@login_required
def addBook(request):
    if request.method == "POST":
        book = makeBookFromRequest(request)
        catalog = PersistentCatalog()
        catalog.add(book)
        return HttpResponse(status=200)
    return HttpResponse("Not found", status=404)


@login_required
def removeBook(request):
    if request.method == "POST":
        book = makeBookFromRequest(request)
        catalog = PersistentCatalog()
        catalog.removeAllByTitle(book.title)
        return HttpResponse(status=200)
    return HttpResponse("Not found", status=404)


def makeBookFromRequest(request):
    title = request.POST.get("title")
    author = request.POST.get("author")
    releaseYear = request.POST.get("releaseYear")
    return Book(title, author, releaseYear)

@csrf_exempt
def createUser(request):
    # Django checks host to be equal to localhost (can only create user from the same machine) in production
    if request.method == "POST":
        if request.META.get('HTTP_X_FORWARDED_FOR') and \
                request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0] != "127.0.0.1":
            return HttpResponse("User creation not allowed from outside localhost", status=401)
        elif request.META.get('REMOTE_ADDR') != "127.0.0.1":
            return HttpResponse("User creation not allowed from outside localhost", status=401)
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            if User.objects.filter(username=username).exists():
                return HttpResponse("User already exists", status=409)
            else:
                try:
                    User.objects.create_user(username=username, password=password)
                    return HttpResponse("User created", status=201)
                except Exception as e:
                    return HttpResponse(str(e), status=500)


    else:
        return HttpResponse("Not found", status=404)
