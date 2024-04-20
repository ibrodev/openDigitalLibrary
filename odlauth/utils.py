from django.db import models

class UserType(models.TextChoices):
    USER = "USER", "User"
    AUTHOR = "AUTHOR", "Author"
    PUBLISHER = "PUBLISHER", "Publisher"
    ADMIN = "ADMIN", "Admin"