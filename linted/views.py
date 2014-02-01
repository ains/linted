from django.http import HttpResponse
from linted.tasks import add


def index(request):
    add.delay(1, 100)
    return HttpResponse("Hello, world. You're at the polls index.")