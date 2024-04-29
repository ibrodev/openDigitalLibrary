from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout as dlogout, authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_control
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from .utils import TokenGenerator, send_activation_email
from .forms import AuthorUserForm, AuthorForm, EmailAccountForm, PublisherForm, PublisherUserForm, PhoneNumberForm, UserAuthenticationForm
from .models import User, Author, Publisher, EmailAccount, PhoneNumber, Profile
from .tasks import send_activation_link

@cache_control(no_cache=True, must_revalidate=True)
def logout(request):
    dlogout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required()
def activate_account(request, token):
    
    user = request.user
        
    if user and TokenGenerator().check_token(user=user, token=token):
        email = user.email
        email.is_confirmed = True
        email.save()
        
        messages.add_message(request=request, level=messages.SUCCESS, message='Congratulations! Your account is activated.')
        
        return redirect(reverse('odlauth:account'))

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
            
            user = authenticate(request, username=user.username, password=user_form.cleaned_data['password1'])
            # send_activation_email(user, request)
            
            send_activation_link.delay({
                'username': user.get_username(), 
                'email': user.email.email,
                'domain': get_current_site(request).domain,
                'token': TokenGenerator().make_token(user=user)
            })
            
            if user is not None:
                login(request, user)
            
                messages.success(request, "Welcome! please confirm your email address")
                return HttpResponseRedirect(reverse("odlauth:account"))
            else:
                messages.error(request, "Error can't login with the registered user")
                
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
            
            user = authenticate(request, username=user.username, password=user_form.cleaned_data['password1'])
            result = send_activation_link.delay({
                'username': user.get_username(), 
                'email': user.email.email,
                'domain': get_current_site(request).domain,
                'token': TokenGenerator().make_token(user=user)
            })
            
            print(result.backend)
            
            if user is not None:
                login(request, user)
            
                messages.success(request, "Welcome! please confirm your email address")
                return HttpResponseRedirect(reverse("odlauth:account"))
            else:
                messages.error(request, "Error can't login with the registered user")

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
        

class UserAccountView(LoginRequiredMixin,View):
    
    def get(self, request, *args, **kwargs):       
        
        return render(request, 'odlauth/pages/account.html')