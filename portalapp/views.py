from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def example_view(request):
    return HttpResponse('I am http response')
