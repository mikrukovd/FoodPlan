from .models import Plan, MenuType, Allergy, User, MealType
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
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()

        if not username or not email:
            messages.error(request, "Имя и e-mail не могут быть пустыми.")
        else:
            user.username = username
            user.email = email
            user.save()
            messages.success(request, "Данные успешно сохранены!")
    
        return redirect("lk")
    
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
    menu_types = MenuType.objects.all()
    allergies = Allergy.objects.all()
    meal_types = MealType.objects.all()

    # Список для отображения
    menu_type_names = [menu_type.name for menu_type in menu_types]
    menu_types_text = ", ".join(menu_type_names)

    context = {
        'menu_types': menu_types,
        'allergies': allergies,
        'meal_types': meal_types,
        'menu_types_text': menu_types_text,
        'menu_types_count': menu_types.count(),
    }

    if request.method == 'POST':
        food_type_id = request.POST.get('foodtype')
        duration = int(request.POST.get('duration', 1))
        persons = int(request.POST.get('persons', 1))
        calories = int(request.POST.get('calories', 2000))

        allergy_ids = request.POST.getlist('allergies')
        food_type = MenuType.objects.filter(id=food_type_id).first()
        if not food_type:
            food_type = MenuType.objects.first()

        # Для теста заглушка
        user, created = User.objects.get_or_create(
            email='demo@example.com',
            defaults={'name': 'Демо пользователь'}
        )

        plan = Plan.objects.create(
            user=user,
            name=f"План питания {food_type.name}",
            food_type=food_type,
            persons=persons,
            calories=calories,
            duration=duration
        )

        for meal_type in meal_types:
            field_name = f"has_{meal_type.name.lower()}"
            is_selected = request.POST.get(field_name) == 'true'
            setattr(plan, field_name, is_selected)
        plan.save()

        if allergy_ids:
            selected_allergies = Allergy.objects.filter(id__in=allergy_ids)
            plan.user_allergies.set(selected_allergies)

        context['success_message'] = f"План питания'{plan.name}' был оплачен и успешно создан!"

    return render(request, 'order.html', context)
