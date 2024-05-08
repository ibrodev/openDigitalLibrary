from django.contrib import admin

from .models import Category, SubCategory, Book

class CategoryAdmin(admin.ModelAdmin):
    pass

class SubCategoryAdmin(admin.ModelAdmin):
    pass


class BookAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
