from django.shortcuts import render
from django.http import HttpResponse
from tasks import add


def index(request):
    add.delay(1, 100)
    return HttpResponse("Hello, world. You're at the polls index.")