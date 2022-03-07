from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

def view_name(request):
    return render(request, 'template_name.html', {})