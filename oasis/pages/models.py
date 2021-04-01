from django.db import models
import uuid # Required for unique listings
from django.forms import ModelForm
from django.urls import reverse


# Create your models here.

# class User(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name 


class Listing(models.Model):
    #fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='unique id for this listing')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    # not yet sure how users work - may want users not to be a model and instead use django default user handling
    # posted_by = models.ForeignKey('User', on_delete=models.SET_NULL,null=True)

    CONDITION = (
        ('1', 'New'),
        ('2', 'Like New'),
        ('3', 'Lightly Used'),
        ('4', 'Moderately Used'),
        ('5', 'Heavily Used')
    )
    condition = models.CharField(
        max_length=1,
        choices=CONDITION,
        blank=True,
        default=1,
        help_text='Book condition',
    )
    # not yet sure yet how to handle images 
    # image = 

    class Meta:
        ordering = ['-date_added']

    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('listings-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return f'{self.id} ({self.book.title})'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    #if we decide to have a model for author:
    #author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    edition = models.CharField(max_length=5) #length here assumes no more than 999th edition -- seems like a reasonable assumption
    pub_year = models.SmallIntegerField() 

    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
