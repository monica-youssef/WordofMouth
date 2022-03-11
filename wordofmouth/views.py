from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello, world. You're at the word of mouth index.")


def homeview(request):
    return render(request, 'wordofmouth.html', {})