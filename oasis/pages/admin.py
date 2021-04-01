from django.contrib import admin

# Register your models here.

from .models import Listing, Book

admin.site.register(Listing)
admin.site.register(Book)
