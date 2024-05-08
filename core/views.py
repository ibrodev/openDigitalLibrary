from django.shortcuts import render

from django.http.request import HttpRequest

from library.models import Book, Category, BookStatus 

def index(request:HttpRequest):
    
    books = Book.objects.filter(status=BookStatus.ACCEPTED).order_by('-published_on')
    
    
    return render(request, 'index.html', {'books': books})
