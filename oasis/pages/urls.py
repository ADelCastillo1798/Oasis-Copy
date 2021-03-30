from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('clientcreation/', views.clientcreation, name='clientcreation'),
    path('login/', views.login, name='login'),


]
