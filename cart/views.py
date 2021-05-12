from django.shortcuts import render, redirect
from pages.models import Listing
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect



@login_required(login_url="/pages/login")
def cartadd(request, id):
    cart = Cart(request)
    product = Listing.objects.get(id=id)
    cart.add(product=product)
    return redirect("/cart/cart-detail/")


@login_required(login_url="/pages/login")
def itemclear(request, id):
    cart = Cart(request)
    product = Listing.objects.get(id=id)
    cart.remove(product)
    return redirect('/cart/cart-detail/')

@login_required(login_url="/pages/login")
def cartdetail(request):
    cart = Cart(request)
    products = []
    context = { 'cart': cart }
    context['products'] = products
    return render(request, 'cart_detail.html', context)
    #return render(request, 'cart_detail.html')
