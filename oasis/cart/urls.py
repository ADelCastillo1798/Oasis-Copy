from django.urls import path
from . import views

app_name = "cart"


urlpatterns = [
    path('cart/add/<uuid:id>/', views.cartadd, name='cartadd'),
    path('cart/item-clear/<uuid:id>/', views.itemclear, name='itemclear'),
    path('cart/cart-detail/',views.cartdetail, name='cartdetail'),

]