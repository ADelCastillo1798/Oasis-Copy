from django.shortcuts import render, redirect
from pages.models import Listing
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

@login_required(login_url="/pages/login")
def cartadd(request, id):
    cart = Cart(request)
    product = Listing.objects.get(id=id)
    cart.add(product=product)
    return redirect("/")


@login_required(login_url="/pages/login")
def itemclear(request, id):
    cart = Cart(request)
    product = Listing.objects.get(id=id)
    cart.remove(product)
    return redirect("cartdetail")

@login_required(login_url="/pages/login")
def cartdetail(request):
    return render(request, 'cart_detail.html')
