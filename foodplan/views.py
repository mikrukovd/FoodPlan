from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'auth.html')


def registration(request):
    return render(request, 'registration.html')


def lk(request):
    return render(request, 'lk.html')


def card1(request):
    return render(request, 'card1.html')


def card2(request):
    return render(request, 'card2.html')


def card3(request):
    return render(request, 'card3.html')


def order(request):
    return render(request, 'order.html')
