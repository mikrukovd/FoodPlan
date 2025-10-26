from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя пользователя"
    )
    email = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Электронная почта"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Allergy(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Название аллергии"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Аллергия"
        verbose_name_plural = "Аллергии"


class MenuType(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Тип меню"
    )
    image = models.ImageField(
        upload_to='menu_types/',
        blank=True,
        null=True,
        verbose_name="Изображение типа меню"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип меню"
        verbose_name_plural = "Типы меню"


class Dish(models.Model):
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Название блюда"
    )
    image = models.ImageField(
        upload_to='dishes/',
        blank=True,
        null=True,
        verbose_name="Изображение блюда"
    )
    descriptions = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание блюда"
    )
    recipe = models.TextField(
        blank=True,
        null=True,
        verbose_name="Рецепт"
    )
    calories = models.BigIntegerField(
        blank=True,
        null=True,
        verbose_name="Калории"
    )
    food_type = models.ForeignKey(
        MenuType,
        on_delete=models.CASCADE,
        verbose_name="Тип пищи"
    )
    containce_allergies = models.ManyToManyField(
        Allergy,
        blank=True,
        related_name="dishes_containing",
        verbose_name="Содержащиеся аллергии"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Название ингредиента"
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Блюдо"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"


class Plan(models.Model):
    DURATION_CHOICES = [
        (1, "1 месяц"),
        (3, "3 месяца"),
        (6, "6 месяцев"),
        (12, "12 месяцев"),
    ]

    PERSONS_CHOICES = [
        (1, "1 персона"),
        (2, "2 персоны"),
        (3, "3 персоны"),
        (4, "4 персоны"),
        (5, "5 персон"),
        (6, "6 персон"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="plans",
        verbose_name="Пользователь"
    )
    name = models.CharField(
        max_length=100,
        default="План питания",
        verbose_name="Название плана"
    )
    food_type = models.ForeignKey(
        MenuType,
        on_delete=models.CASCADE,
        verbose_name="Тип пищи"
    )
    persons = models.IntegerField(
        choices=PERSONS_CHOICES,
        default=1,
        verbose_name="Количество персон"
    )
    user_allergies = models.ManyToManyField(
        Allergy,
        blank=True,
        verbose_name="Аллергии пользователя"
    )
    calories = models.IntegerField(
        verbose_name="Калории"
    )
    has_breakfast = models.BooleanField(
        default=True,
        verbose_name="Включает завтрак"
    )
    has_lunch = models.BooleanField(
        default=True,
        verbose_name="Включает обед"
    )
    has_dinner = models.BooleanField(
        default=True,
        verbose_name="Включает ужин"
    )
    has_dessert = models.BooleanField(
        default=True,
        verbose_name="Включает десерт"
    )
    duration = models.IntegerField(
        choices=DURATION_CHOICES,
        default=1,
        verbose_name="Продолжительность"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "План питания"
        verbose_name_plural = "Планы питания"


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь"
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="План питания"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания"
    )
    ends_at = models.DateTimeField(
        verbose_name="Дата окончания"
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Активна"
    )

    def __str__(self):
        return f"{self.user} - {self.plan}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class MealType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Тип приема пищи"
    )
    is_default = models.BooleanField(
        default=True,
        verbose_name="Включен по умолчанию"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип приема пищи"
        verbose_name_plural = "Типы приемов пищи"
