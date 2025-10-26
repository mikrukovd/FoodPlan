from django.shortcuts import render
from .models import Plan, MenuType, Allergy, User, MealType

# Create your views here.


def index(request):
    return render(request, 'index.html')


def auth(request):
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
