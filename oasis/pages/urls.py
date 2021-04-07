from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('clientcreation/', views.clientcreation, name='clientcreation'),
    path('messaging/', views.messaging, name='messaging'),
    path('landing/', views.landingpage, name = 'landingpage'),
    path('login/', views.loginview, name = 'login'),
    path('search/', views.search, name = 'search'),
    path('listings/', views.ListingView.as_view(), name='listings'),
    path('listings/<str:pk>', views.ListingDetailView.as_view(), name='listings-detail'),
]
