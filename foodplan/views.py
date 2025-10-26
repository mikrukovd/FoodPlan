from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User


def index(request):
    return render(request, 'index.html')


def auth(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if not email:
            messages.error(request, 'Введите email')
            return render(request, 'auth.html')

        try:

            user = User.objects.get(email=email)
            messages.success(request, f'Добро пожаловать, {user.name or user.email}!')

        except User.DoesNotExist:
            # СОЗДАЕМ НОВОГО пользователя
            user = User.objects.create(
                email=email,
                name=email.split('@')[0]  # Имя из email
            )
            messages.success(request, 'Новый аккаунт создан! Дополните информацию в личном кабинете.')

        # Создаем сессию для пользователя
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['user_name'] = user.name or ''

        return redirect('index')

    return render(request, 'auth.html')


def logout_view(request):
    # Очищаем сессию
    request.session.flush()
    messages.success(request, 'Вы вышли из системы')
    return redirect('index')


def login_required_custom(function):
    def wrap(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, 'Для доступа к этой странице необходимо авторизоваться')
            return redirect('auth')
        return function(request, *args, **kwargs)

    return wrap


@login_required_custom
def lk(request):
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'Пользователь не найден')
        return redirect('auth')

    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.save()
        messages.success(request, 'Данные обновлены!')
        request.session['user_name'] = user.name or ''
        return redirect('lk')

    return render(request, 'lk.html', {'user': user})


def card1(request):
    return render(request, 'card1.html')


def card2(request):
    return render(request, 'card2.html')


def card3(request):
    return render(request, 'card3.html')


@login_required_custom
def order(request):
    return render(request, 'order.html')
