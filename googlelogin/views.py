from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def loginview(request):
    return render(request, 'googlelogin.html', {})