from django.shortcuts import render, redirect

from pages.models import Book, Listing

from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm
from .forms import ListForm
from django.contrib import messages



# Create your views here.

def home(request):

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()

    context = {
        'num_books': num_books,
        'num_listings': num_listings,
    }


    return render(request, 'index.html', context=context)

def clientcreation(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'clientcreation.html', {'form': form})

def loginview(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
   

def landingpage(request):
    return render(request, 'LandingPage.html')


def messaging(request):
    return render(request, 'messaging.html')

def search(request):
    return render(request, 'search.html')

class ListingView(generic.ListView):
    model = Listing 
    context_object_name = 'listing_view'
    queryset = Listing.objects.all() 
    template_name = 'listings_view.html'  # Specify your own template name/location

class ListingDetailView(generic.DetailView):
    model = Listing
    template_name = 'listings_detail_view.html'

def sellerlisting(request):
    if request.method == 'POST':
        form = ListForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            isbn = form.cleaned_data.get('isbn')
            edition = form.cleaned_data.get('edition')
            pub_year = form.cleaned_data.get('pub_year')
            condition =form.cleaned_data.get('condition')
            new_book = Book(title=title, author=author, isbn=isbn, edition=edition, pub_year=pub_year)
            new_book.save() 
            new_listing = Listing(book=new_book, condition=condition)
            new_listing.user = request.user
            new_listing.save() 
            return redirect('/')
    else:
        form = ListForm()
    return render(request, 'sellerlisting.html', {'form': form})
