from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.home, name='index'),
    path('clientcreation/', views.clientcreation, name='clientcreation'),
    path('messaging/', views.messaging, name='messaging'),
    path('landing/', views.landingpage, name='landingpage'),
    path('login/', views.loginview, name='login'),
    path('search/', views.search, name='search'),
    path('listings/', views.ListingView.as_view(), name='listings'),
    # path('chat/', views.chat, name='chat'),
    # path('messaging/<str:conversation_id>/', views.chat, name='chat2'),
    path('chat/<str:conversation_id>/', views.chat, name='chat'),
    path('messaging', views.messaging, name='messaging'),
    path(
        'listings/<str:pk>',
        views.ListingDetailView.as_view(),
        name='listings-detail'),
    path('sellerlisting/', views.sellerlisting, name='sellerlisting'),
    path('profile/', views.profile, name='profile'),
    path(
        'newconversation/<uuid:id>/',
        views.newconversation,
        name='newconversation'),
    path('admin/', views.admin, name='admin'),
    path('report/<uuid:oid>/', views.reportlisting, name='reportlisting'),
    path(
        'messaging/closeconversation/<str:user_id>/<uuid:conversation_id>',
        views.closeconversation,
        name='closeconversation'),
    path('newconversation/<uuid:id>/', views.newconversation, name='newconversation'),
    path('newuserconversation/<int:oid>/', views.newuserconversation, name='newuserconversation'),
    path('admin/', views.admin, name='admin'),
    path('report/<uuid:oid>/', views.reportlisting, name='reportlisting'),
    path('clearListing/<uuid:oid>/', views.clearlisting, name='clearlisting'),
    path('removeListing/<uuid:oid>/', views.removelisting, name='removelisting'),
    path('logout/', views.logout_user, name='logout'),
    path('ban_user/<int:oid>/', views.ban_user, name='ban_user'),

]
