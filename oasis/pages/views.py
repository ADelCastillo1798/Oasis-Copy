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

def landingpage(request):
    return render(request, 'LandingPage.html')

def login(request):
    return render(request, 'login.html')

def messaging(request):
    return render(request, 'messaging.html')

def search(request):
    return render(request, 'search.html')