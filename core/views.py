from django.shortcuts import render

from django.http.request import HttpRequest
from django.http.response import HttpResponse

def index(request:HttpRequest):
    
    return render(request, 'index.html')