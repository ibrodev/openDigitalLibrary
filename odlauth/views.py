from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as dlogout

from .forms import AuthorUserForm, AuthorForm, EmailAccountForm, PublisherForm, PublisherUserForm, PhoneNumberForm, UserAuthenticationForm

def logout(request):
    dlogout(request)
    return HttpResponseRedirect(reverse('index'))

class UserLoginView(LoginView):
    template_name = 'odlauth/pages/login.html'
    authentication_form = UserAuthenticationForm
    redirect_authenticated_user = True

        
class AccountView(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, 'odlauth/pages/account_type.html')
    
    def post(self, request, *args, **kwargs):
        print(request.POST['account_type'])
        if request.POST['account_type'] == "author":
            return HttpResponseRedirect(reverse("odlauth:new_account_author"))
        
        if request.POST['account_type'] == "publisher":
            return HttpResponseRedirect(reverse("odlauth:new_account_publisher"))
        
        else:
            return HttpResponseNotFound()
        

class AuthorAccountView(View):
    
    def get(self, request, *args, **kwargs):
        
        account_form = AuthorForm()
        email_form = EmailAccountForm()
        phone_form = PhoneNumberForm()
        user_form = AuthorUserForm()
        
        return render(
            request, 
            'odlauth/pages/registration.html',
            {
                "user_form": user_form, 
                "account_form":account_form,
                "email_form": email_form,
                "phone_form": phone_form,
                "url": "odlauth:new_account_author"
            }
        )
    
    def post(self, request, *args, **kwargs):
        
        account_form = AuthorForm(request.POST)
        email_form = EmailAccountForm(request.POST)
        user_form = AuthorUserForm(request.POST)
        phone_form = PhoneNumberForm(request.POST)
        
        
        if account_form.is_valid() and email_form.is_valid() and user_form.is_valid() and phone_form.is_valid():
            
            email = email_form.save()
            phone = phone_form.save()
            account = account_form.save(commit=False)
            user = user_form.save(commit=False)
            
            account.email = email
            account.phone_no = phone
            account.save()
            
            user.email = email
            user.save()
            
            return HttpResponseRedirect(reverse("index"))

        return render(
            request, 
            'odlauth/pages/registration.html',
            {
                "user_form": user_form, 
                "account_form":account_form,
                "phone_form": phone_form,
                "email_form": email_form,
                "url": "odlauth:new_account_author"
            }
        )
    

class PublisherAccountView(View):
    
    def get(self, request, *args, **kwargs):
        
        account_form = PublisherForm()
        email_form = EmailAccountForm()
        user_form = PublisherUserForm()
        
        return render(
            request, 
            'odlauth/pages/registration.html',
            {
                "user_form": user_form, 
                "account_form": account_form,
                "email_form":email_form,
                "url": "odlauth:new_account_publisher"
            }
        )
    
    def post(self, request, *args, **kwargs):
        
        account_form = PublisherForm(request.POST)
        email_form = EmailAccountForm(request.POST)
        user_form = PublisherUserForm(request.POST)
        
        
        if account_form.is_valid() and email_form.is_valid() and user_form.is_valid():
            
            email = email_form.save()
            account = account_form.save(commit=False)
            user = user_form.save(commit=False)
            
            account.email = email
            account.save()
            
            user.email = email
            user.save()
            
            return HttpResponseRedirect(reverse("index"))

        return render(
            request, 
            'odlauth/pages/registration.html',
            {
                "user_form": user_form, 
                "account_form":account_form,
                "email_form": email_form,
                "url": "odlauth:new_account_publisher"
            }
        )