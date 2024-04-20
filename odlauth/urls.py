from django.urls import path
from .views import AccountView, AuthorAccountView, PublisherAccountView, UserLoginView, logout

app_name = 'odlauth'
urlpatterns = [
    path('new/', AccountView.as_view(), name="new_account"),
    path('new/author/', AuthorAccountView.as_view(), name="new_account_author"),
    path('new/publisher/', PublisherAccountView.as_view(), name="new_account_publisher"),
    
    path('login/', UserLoginView.as_view(), name="account_login"),
    path('logout/', logout, name="account_logout"),
]
