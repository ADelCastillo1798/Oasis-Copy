from django.shortcuts import render, redirect

from pages.models import Book, Listing, Conversation, Message, User, ReportListing, NumSearch

from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .forms import ListForm
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json 
from cart.cart import Cart



def home(request):

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()

    context = {
        'num_books': num_books,
        'num_listings': num_listings,
        'num_users': User.objects.all().count(),
    }

    return render(request, 'index.html', context=context)


def clientcreation(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            login(request, username)
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
            user_ = authenticate(username=username, password=password)
            login(request, user_)
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

    def get_queryset(self, *args, **kwargs):
        val = self.request.GET.get("q")
        if val:
            queryset = Listing.objects.filter(
                Q(book__title__icontains=val) |
                Q(book__author__icontains=val) |
                Q(book__isbn__icontains=val)
                ).distinct()
            for i in NumSearch.objects.all():
                i.count = i.count + 1
                i.save()
        else:
            queryset = Listing.objects.all()
        return queryset


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
            condition = form.cleaned_data.get('condition')
            price = form.cleaned_data.get('price')
            new_book = Book(
                title=title,
                author=author,
                isbn=isbn,
                edition=edition,
                pub_year=pub_year)
            new_book.save()
            new_listing = Listing(book=new_book, condition=condition, price=price)
            new_listing.user = request.user
            new_listing.save()
            return redirect('/')
    else:
        form = ListForm()
    return render(request, 'sellerlisting.html', {'form': form})


def chat(request, conversation_id):
    # conversation, is_new = Conversation.objects.get_or_create(id=conversation_id)
    # reversed(conversation.message_set.order_by('-timestamp')[:50])

    return render(
        request,
        'chat.html',
        {
            'conversation_id': conversation_id
            # 'conversation': conversation,
            # 'conversation_id': conversation_id,
            # 'messages': conversation.message_set,
        })

@login_required(login_url="/pages/login")
def messaging(request):
    #get current user
    current_user = request.user
    #get all conversations involving the current user
    conversations = Conversation.objects.filter(
        seller=current_user) | Conversation.objects.filter(buyer=current_user)
    #get all messages for each conversation
    #this way seems inefficient and there's probably a way to only load messages on demand with javascript BUT i have not found it
    message_list = []
    for conversation in conversations:
        # print(conversation.message_set.all().values())
        message_list.append([conversation.id,list(conversation.message_set.values())])
    messages = json.dumps(message_list, cls=DjangoJSONEncoder)
    
    return render(request, 'messaging.html', {
        'current_user': current_user,
        'conversations': conversations,
        'messages': messages
    })

@login_required(login_url="/pages/login")
def newconversation(request, id):
    posted_by = Listing.objects.get(id=id).user
    conversation, is_new = Conversation.objects.get_or_create(id=id, seller = posted_by, buyer=request.user)
    return redirect("/pages/messaging")

def profile(request):
    if(request.user.is_authenticated):
        num_books = Book.objects.all().count()
        num_listings = Listing.objects.all().count()
        listings = Listing.objects.all()
        cart = Cart(request)
        cart_item = []
        item = Listing.objects.all()
        for i in cart:
            cart_item.append(i['product'].id)
        for j in cart_item:
            item = item.exclude(id = j)
        item = item.exclude(user = request.user)
        if(len(item)>3):
            item = item.order_by("?")[:3]
        my_books = listings.filter(user = request.user)
    else:
        return redirect('/pages/login/')
    vars = {
        'num_books':num_books,
		'num_listings':num_listings,
		'num_users':User.objects.all().count(),
		'listings':listings,
		'cart':cart,
		'left':item,
        'my_books':my_books
    }
    return render(request, 'profile.html', context=vars)

def admin(request):
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()
    listings = Listing.objects.all()
    item = []
    item = listings.exclude(report = None)
    vars = {
        'num_books':num_books,
		'num_listings':num_listings,
		'num_users':User.objects.all().count(),
		#'report':ReportListing.objects.all()
        'report':item,
        'searches':NumSearch.objects.all(),
    }
    return render(request, 'admin_view.html', context=vars)

def reportlisting(request, oid):
    reportedlisting = Listing.objects.filter(id=oid).first()
    new_report = ReportListing()
    new_report.sent_by = request.user
    new_report.save()
    reportedlisting.report = new_report
    reportedlisting.times_reported = reportedlisting.times_reported + 1
    reportedlisting.save()
    return redirect('/')

def clearlisting(request, oid):
    item = []
    item = Listing.objects.all().exclude(report = None)
    item = item.filter(id=oid)
    for i in item:
        i.report.delete()
    return redirect('/pages/admin/')

def removelisting(request, oid):
    item = []
    item = Listing.objects.all().exclude(report = None)
    item = item.filter(id=oid)
    for i in item:
        book = i.book
        i.delete()
        book.delete()
    return redirect('/pages/admin/')

def logout_user(request):
    logout(request)
    return redirect('/pages/')

def ban_user(request, oid, lid):
    u = User.objects.all().filter(id=oid)
    for i in u:
        i.delete()
    item = Listing.objects.all().filter(id=lid)
    for i in item:
        book = i.book
        i.delete()
        book.delete()
    return redirect('/pages/admin/')
