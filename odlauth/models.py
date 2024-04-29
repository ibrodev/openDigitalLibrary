from typing import Collection
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .utils import UserType


class EmailAccount(models.Model):
    email = models.EmailField(max_length=255,unique=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email

class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    is_confirmed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.phone_number

class UserManager(BaseUserManager):
    
    def create_user(self, username, password, **kwargs):
        
            
        if not username:
            raise ValueError("users must have a username")

        user = self.model(
            username=username,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, password):

        user = self.create_user(
            username=username,
            password=password,
            is_superuser =True,
            is_staff = True,
            user_type = UserType.SUPERUSER
        )
        
        user.save(using=self._db)
        
            
        return user
    
class User(AbstractBaseUser):
    
    default_user_type = UserType.USER
    
    first_name = None
    last_name = None
        
    username = models.CharField(max_length=200, unique=True)
    user_type = models.CharField(max_length=50, choices=UserType.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateField(auto_created=True, auto_now=True)
    email = models.OneToOneField(EmailAccount, on_delete=models.CASCADE, null=True, blank=True)
    
    USERNAME_FIELD = "username"
    
    objects = UserManager()
    
    def get_email(self):
        return self.email.email
    
    def get_username_first_letter(self):
        return self.get_username().capitalize()[0]
        
    def __str__(self):
        return self.get_username()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.user_type:
            self.user_type = self.default_user_type
        return super().save(*args, **kwargs)
    
    
    def is_author(self):
        return self.user_type == UserType.AUTHOR

    def is_publisher(self):
        return self.user_type == UserType.PUBLISHER
    
    def is_email_confirmed(self):
        
        return self.email and self.email.is_confirmed
            
    


class AuthorUserManager(UserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(user_type=UserType.AUTHOR)

class AuthorUser(User):
    
    default_user_type = UserType.AUTHOR
    
    objects = AuthorUserManager()
    
    class Meta:
        proxy = True

class PublisherUserManager(UserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(user_type=UserType.PUBLISHER)
        
class PublisherUser(User):
    
    default_user_type = UserType.PUBLISHER
    
    objects = PublisherUserManager()
    
    class Meta:
        proxy = True
        

class AdminUserManager(UserManager):

    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(user_type=UserType.ADMIN)

class AdminUser(User):
    
    default_user_type = UserType.ADMIN
    
    objects = AdminUserManager()
    class Meta:
        proxy = True
        
    
class Author(models.Model):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.OneToOneField(EmailAccount, on_delete=models.CASCADE)
    phone_no = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)
    bio = models.TextField('author biography', blank=True, null=True)
    profile_pic = models.FileField(blank=True, null=True)
    
    
    def __str__(self):
        return self.get_full_name()
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name
    
class Publisher(models.Model):
    
    name = models.CharField(max_length=255, unique=True)
    email = models.OneToOneField(EmailAccount, on_delete=models.CASCADE, null=True, blank=True)
    phone_no = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True, unique=True)
    profile_pic = models.FileField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    
class Profile(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.FileField(blank=True, null=True)
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    