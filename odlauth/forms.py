from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import User, AuthorUser, PublisherUser, AdminUser, EmailAccount, PhoneNumber, Author, Publisher, Profile

class ODLForm(forms.Form):
    template_name = "odlauth/forms/form_snippet.html"

class ODLModelForm(ODLForm, forms.ModelForm):
    pass

class UserAuthenticationForm(ODLForm, AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "This account is inactive.",
                code="inactive",
            )

class AuthorForm(ODLModelForm):
    
    class Meta:
        model = Author
        fields = ['first_name', 'last_name']
        
    def save(self, commit=True):
        return super().save(commit)

class PublisherForm(ODLModelForm):

    class Meta:
        model = Publisher
        fields = ['name']
        
    def save(self, commit=True):
        return super().save(commit)

# TODO: Come back here
# class ProfileForm(ODLModelForm):

#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name']
        
#     def save(self, commit=True):
#         return super().save(commit)


class EmailAccountForm(ODLModelForm):

    class Meta:
        model = EmailAccount
        fields = ['email']
        
    def save(self, commit=True):
        return super().save(commit)

class PhoneNumberForm(ODLModelForm):

    class Meta:
        model = PhoneNumber
        fields = ['phone_number']
        
    def save(self, commit=True):
        return super().save(commit)

class UserForm(ODLModelForm):
    
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class AuthorUserForm(UserForm):
    
    class Meta:
        model = AuthorUser
        fields = ["username"]
    
    def save(self, commit=True):
        return super().save(commit)    
        
class PublisherUserForm(UserForm):
    
    class Meta:
        model = PublisherUser
        fields = ["username"]
        
    def save(self, commit=True):
        return super().save(commit)