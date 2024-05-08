from django.forms import ModelForm, FileField, FileInput

from .models import Book

class BookForm(ModelForm):
    template_name = "odlauth/forms/form_snippet.html"
    
    file = file = FileField(widget=FileInput(attrs={'accept':'application/pdf'}))
    
    class Meta:
        model = Book
        fields = ['title','file','cover','sub_category','authors','publisher','description']