from django.urls import path

from .views import AddBookView, ViewBook

app_name = 'library'
urlpatterns = [
    path('add_book/', AddBookView.as_view(), name="add_book"),
    path('book/<int:id>/', ViewBook.as_view(), name="view_book"),
]
