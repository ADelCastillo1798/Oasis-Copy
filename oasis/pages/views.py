from django.shortcuts import render

from pages.models import User, Book, Listing

from django.views import generic

# Create your views here.

def index(request):

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()
    num_users = User.objects.all().count()

    context = {
        'num_books': num_books,
        'num_listings': num_listings,
        'num_users': num_users
    }


    return render(request, 'index.html', context=context)


def clientcreation(request):

    return render(request, 'clientcreation.html')