from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.auth_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('lk/', views.lk, name='lk'),
    path('logout/', views.logout_view, name='logout'),
    path('card1/', views.card1, name='card1'),
    path('card2/', views.card2, name='card2'),
    path('card3/', views.card3, name='card3'),
    path('order/', views.order, name='order'),
]
