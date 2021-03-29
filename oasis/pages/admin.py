from django.contrib import admin

# Register your models here.

from .models import User, Listing, Book

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Book)
