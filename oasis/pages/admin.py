from django.contrib import admin

# Register your models here.

from .models import Listing, Book, Conversation, Message

admin.site.register(Listing)
admin.site.register(Book)
admin.site.register(Conversation)
admin.site.register(Message)