from django.shortcuts import render, redirect

from pages.models import User, Book, Listing

from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import RegistrationForm
from .forms import UserRegistrationForm
from django.contrib import messages



# Create your views here.

def home(request):

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
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request)
            return redirect('/')
    else:
        form = UserRegistrationForm()
    return render(request, 'clientcreation.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "login.html",
                    context={"form":form})

    return render(request, 'clientcreation.html')

def landingpage(request):
    return render(request, 'LandingPage.html')


def messaging(request):
    return render(request, 'messaging.html')

def search(request):
    return render(request, 'search.html')
