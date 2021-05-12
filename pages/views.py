from django.shortcuts import render, redirect

from pages.models import Book, Listing, Conversation, Message, User, ReportListing, NumSearch, Profile

from django.views import generic
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .forms import ListForm, FilterForm
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import json
from cart.cart import Cart
from django.contrib import messages



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
            email = form.cleaned_data.get('email')
            if not email.endswith("@bc.edu"):
                messages.error(request,'email must be a boston college email')
                return redirect('/pages/clientcreation')
            new_user =form.save()
            username = form.cleaned_data.get('username')
            login(request, new_user)
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


        queryset = Listing.objects.all()
        
        if self.request.GET.get('Price: Low to High') == 'Price: Low to High':
            queryset = queryset.order_by('price')

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
        
		
        condition_field = self.request.GET.get('condition_field')
        title_field = self.request.GET.get('title_field')
        author_field = self.request.GET.get('author_field')
        edition_field = self.request.GET.get('edition_field')

        #print(title_field)
        #title_field = title_field['book__title']
        if condition_field is None or condition_field is '0':
            queryset = queryset
        else:
            queryset = queryset.filter(condition=condition_field)

        if title_field is None or title_field is '':
            queryset = queryset
        else:

            queryset = queryset.filter(book__title=title_field)

        if author_field is None or author_field is '':
            queryset = queryset
        else:
            queryset = queryset.filter(book__author=author_field)

        if edition_field is None or edition_field is '':
            queryset = queryset
        else:
            queryset = queryset.filter(book__edition=edition_field)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={
            'condition_field': self.request.GET.get('condition_field', ''),
            'title_field': self.request.GET.get('title_field', ''),
            'author_field': self.request.GET.get('author_field', ''),
            'edition_field': self.request.GET.get('edition_field', ''),

        })

        return context




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
            confirm_isbn = form.cleaned_data.get("confirm_isbn")
            avatar_url = request.form["avatar-url"]
            if isbn != confirm_isbn:
                messages.error(request,'isbn do not match')
                return redirect('/pages/sellerlisting')
            new_book = Book(
                title=title,
                author=author,
                isbn=isbn,
                edition=edition,
                pub_year=pub_year)
            new_book.save()
            new_listing = Listing(
                book=new_book, condition=condition, price=price)
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
        message_list.append(
            [conversation.id,
             list(conversation.message_set.values())])
    messages = json.dumps(message_list, cls=DjangoJSONEncoder)

    return render(request, 'messaging.html', {
        'current_user': current_user,
        'conversations': conversations,
        'messages': messages
    })


def closeconversation(request, user_id, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)
    print(conversation.seller.id, conversation.buyer.id, user_id)
    print(type(conversation.seller.id), type(user_id))
    if str(conversation.seller.id) == user_id:
        if conversation.state == '0':  #conversation is active
            conversation.state = '2'  #change status to marked complete by seller
        elif conversation.state == '1':  #conversation has been marked completed by buyer
            conversation.state = '3'  #change status to complete
        else:
            #conversation has already been marked complete by this user
            print("conversation already marked complete")
    elif str(conversation.buyer.id) == user_id:
        if conversation.state == '0':  #conversation is active
            conversation.state = '1'  #change status to marked complete by seller
        elif conversation.state == '2':  #conversation has been marked completed by buyer
            conversation.state = '3'  #change status to complete
        else:
            #conversation has already been marked complete by this user
            print("conversation already marked complete")
    else:
        print(
            "Something's gone wrong. Only the seller and buyer should have access to this converation."
        )
    return redirect("/pages/messaging")


@login_required(login_url="/pages/login")
def newconversation(request, id):
    posted_by = Listing.objects.get(id=id).user
    conversation, is_new = Conversation.objects.get_or_create(
        id=id, seller=posted_by, buyer=request.user)
    return redirect("/pages/messaging")

@login_required(login_url="/pages/login")
def newuserconversation(request, oid):
    target = User.objects.all().filter(id = oid)
    conversation, is_new = Conversation.objects.get_or_create(seller = target[0], buyer=request.user)
    return redirect("/pages/messaging")

def profile(request):
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()
    listings = Listing.objects.all()
    cart = Cart(request)
    cart_item = []
    item = Listing.objects.all()
    for i in cart:
        cart_item.append(i['product'].id)
    for j in cart_item:
        item = item.exclude(id=j)
    if (len(item) > 3):
        item = item.order_by("?")[:3]
    my_books = listings.filter(user=request.user)
    vars = {
        'num_books': num_books,
        'num_listings': num_listings,
        'num_users': User.objects.all().count(),
        'listings': listings,
        'cart': cart,
        'left': item,
        'my_books': my_books,
    }
    return render(request, 'profile.html', context=vars)

def admin(request):
    num_books = Book.objects.all().count()
    num_listings = Listing.objects.all().count()
    listings = Listing.objects.all()
    item = []
    item = listings.exclude(report = None)
    low_buyer = Profile.objects.all().exclude(buyer_rating = 5)
    low_buyer = low_buyer.exclude(buyer_rating = 4)
    low_buyer = low_buyer.exclude(buyer_rating = 3)
    low_seller = Profile.objects.all().exclude(seller_rating = 5)
    low_seller = low_seller.exclude(seller_rating = 4)
    low_seller = low_seller.exclude(seller_rating = 3)
    messageReports = Conversation.objects.all().exclude(report = None)
    vars = {
        'num_books':num_books,
		'num_listings':num_listings,
		'num_users':User.objects.all().count(),
        'report':item,
        'searches':NumSearch.objects.all(),
        'low_buyer':low_buyer,
        'low_seller':low_seller,
        'mes_rep':messageReports,
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

def reportmessage(request, oid):
    reportedmessage = Conversation.objects.filter(id=oid).first()
    new_report = ReportListing()
    new_report.sent_by = request.user
    new_report.save()
    reportedmessage.report = new_report
    reportedmessage.save()
    return redirect('messaging')

def clearlisting(request, oid):
    item = []
    item = Listing.objects.all().exclude(report = None)
    item = item.filter(id=oid)
    for i in item:
        i.times_reported = 0
        i.save()
        i.report.delete()
    return redirect('/pages/admin/')
	
def clearMessage(request, oid):
    item = []
    item = Conversation.objects.all().exclude(report = None)
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

def hidelisting(request, oid):
    item = []
    item = Listing.objects.all().exclude(report = None)
    item = item.filter(id=oid)
    for i in item:
        i.hide_listing=True
        i.save()
    return redirect('/pages/admin/')

def unhidelisting(request, oid):
    item = []
    item = Listing.objects.all().exclude(report = None)
    item = item.filter(id=oid)
    for i in item:
        i.hide_listing=False
        i.save()
    return redirect('/pages/admin/')

def logout_user(request):
    logout(request)
    return redirect('/pages/')

def ban_user(request, oid):
    item = Listing.objects.all().filter(user=oid)
    for i in item:
        book = i.book
        i.delete()
        book.delete()
    u = User.objects.all().filter(id=oid)
    for i in u:
        i.delete()
    return redirect('/pages/admin/')

def inactivate_user(request, oid):
    users = User.objects.filter(id=oid).update(is_active=False)
    return redirect('/pages/admin/')

def activate_user(request, oid):
    users = User.objects.filter(id=oid).update(is_active=True)
    return redirect('/pages/admin/')


