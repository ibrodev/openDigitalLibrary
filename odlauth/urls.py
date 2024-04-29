from django.urls import path
from .views import AccountView, AuthorAccountView, PublisherAccountView, UserLoginView, logout, UserAccountView, activate_account

app_name = 'odlauth'
urlpatterns = [
    path('account/', UserAccountView.as_view(), name="account"),
    path('new/', AccountView.as_view(), name="new_account"),
    path('new/author/', AuthorAccountView.as_view(), name="new_account_author"),
    path('new/publisher/', PublisherAccountView.as_view(), name="new_account_publisher"),
    
    path('login/', UserLoginView.as_view(), name="account_login"),
    path('logout/', logout, name="account_logout"),
    
    path('activate/<token>', activate_account, name="account_activate"),
]
