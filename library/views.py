from uuid import uuid4

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http.response import Http404

from .forms import BookForm
from .models import Book, BookStatus
from odlauth.utils import UserType



class AddBookView(LoginRequiredMixin,View):
    
    def get(self, request, *args, **kwargs):
        
        form = BookForm()
        
        return render(
            request, 
            'library/pages/add_books.html',
            {
                "form": form, 
            }
        )
    
    def post(self, request, *args, **kwargs):
        
        
        form = BookForm(request.POST, request.FILES)
        
        
        if form.is_valid():
            
            book = form.save(commit=False)
            
            if request.user.user_type == UserType.AUTHOR:
                author = request.user.email.author
                book.contributer_author = author
            
            if request.user.user_type == UserType.PUBLISHER:
                publisher = request.user.email.publisher
                book.contributer_publisher = publisher
                
            
            
            book.save()
            
            
            messages.success(request, "Book added successfully!")
            return redirect(reverse('odlauth:account_books'))
                
        return render(
            request, 
            'library/pages/add_books.html',
            {
                "form": form, 
            }
        )
    

class ViewBook(View):
    
    def get(self, request, *args, **kwargs):
        
        book = get_object_or_404(Book, pk=kwargs['id'])
        
        if book.status != BookStatus.ACCEPTED:
            raise Http404()
        
        return render(request, 'library/pages/single_book.html', {'book': book})
    
class SearchView(View):
    
    def get(self, request, *args, **kwargs):
        
        t = request.GET['t'].strip()
                
        if not t and t == '':
            
            return redirect(reverse('index'))
        
        result = Book.objects.filter(status=BookStatus.ACCEPTED).filter(title__icontains=t)
        
        return render(request, 'library/pages/search_result.html', {'result': result, 't': t})