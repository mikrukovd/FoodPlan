from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm
# Create your views here.


def index(request):
    return render(request, 'index.html')


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('lk')
    else:
        form = RegisterForm()

    return render(request, 'registration.html', {'form': form})


def auth_view(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("lk")

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get("email").strip().lower()
        password = form.cleaned_data.get("password")

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            messages.error(request, "Пользователь с таким e-mail не найден.")
            return render(request, "auth.html", {"form": form})

        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth is None:
            messages.error(request, "Неверный e-mail или пароль.")
            return render(request, "auth.html", {"form": form})

        auth_login(request, user_auth)
        messages.success(request, f"Добро пожаловать, {user_auth.username}!")
        return redirect("lk")

    return render(request, "auth.html", {"form": form})


@login_required
def lk(request):
    return render(request, "lk.html")


def logout_view(request):
    auth_logout(request)
    messages.info(request, "Вы вышли из аккаунта.")
    return redirect("index")



def card1(request):
    return render(request, 'card1.html')


def card2(request):
    return render(request, 'card2.html')


def card3(request):
    return render(request, 'card3.html')


def order(request):
    return render(request, 'order.html')


