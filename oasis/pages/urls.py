from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clientcreation/', views.clientcreation, name='clientcreation'),
    path('messaging/', views.messaging, name='messaging'),
    path('landing/', views.landingpage, name = 'landingpage'),
    path('login/', views.login, name = 'login'),
    path('search/', views.search, name = 'search'),
]
