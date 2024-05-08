from django.db import models

from odlauth.models import Author, Publisher

class BookStatus(models.TextChoices):
    ACCEPTED = "ACCEPTED", "Accepted"
    REJECTED = "REJECTED", "Rejected"
    PENDING = "PENDING", "Pending"

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Book(models.Model):     
    title = models.CharField(max_length=300)
    file = models.FileField(verbose_name='Book (PDF format)', upload_to='documents')
    cover = models.ImageField(blank=True, null=True, upload_to='covers')
    sub_category = models.ForeignKey(SubCategory, verbose_name='category', on_delete=models.SET_NULL, blank=True, null=True)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True)
    description = models.TextField(verbose_name='book description')
    status = models.CharField(max_length=50, choices=BookStatus.choices, default=BookStatus.PENDING)
    rejection_reason = models.TextField(null=True, blank=True)
    published_on = models.DateField(auto_now_add=True)
    contributer_author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='book_contributer_author')
    contributer_publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='book_contributer_publisher')
    
    def __str__(self):
        return self.title
