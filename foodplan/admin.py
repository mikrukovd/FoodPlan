from django.contrib import admin
from .models import (
    User, Allergy, MenuType,
    Dish, Ingredient, Plan, Subscription
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_at')
    search_fields = ('email', 'name')


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'food_type', 'calories')
    list_filter = ('food_type',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'dish')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'food_type', 'persons', 'duration')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'created_at', 'is_active')
    list_filter = ('is_active',)
