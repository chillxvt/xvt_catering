from django.db import models
from django.conf import settings
from datetime import date
from django.utils import timezone
from collections import defaultdict


# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    instructions = models.TextField(help_text='Please give instructions on the recipe')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientAmount')
    portions = models.IntegerField()

    def __str__(self):
        return self.name


# Hidden model used for recipe data storage
class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    UNITS_CHOICES = [
        ('gr', 'grams'),
        ('kg', 'kilograms'),
        ('ml', 'milliliters'),
        ('lt', 'liters'),
        ('unt', 'units'),
        ('cl', 'cloves'),
        ('tsp', 'teaspoon'),
        ('cp', 'cup'),
        ('tbl', 'tablespoon')
        # TODO add spoons, cups etc
    ]
    unit = models.CharField(max_length=3, choices=UNITS_CHOICES)
    amount = models.FloatField(blank=False, null=False)

    class Meta:
        unique_together = ('ingredient', 'recipe')


# model used for storing breakfast,lunch or dinner
class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)  # Link to the Custom User Model in the accounts app
    date = models.DateField(auto_now_add=False, blank=True, default=date.today)
    MEAL_CHOICES = [
        ('br', 'Breakfast'),
        ('lu', 'Lunch'),
        ('dr', 'Dinner'),
        ('sn', 'Snack')
    ]
    meal = models.CharField(max_length=3, choices=MEAL_CHOICES)
    recipes = models.ManyToManyField(Recipe, through='Dish')
    extra = models.ManyToManyField(Ingredient, through='ExtraItems')

    class Meta:
        unique_together = ['user', 'date', 'meal']

    @staticmethod
    def extract_ingredient_list(start_date, end_date):
        meals = Meal.objects.filter(date__range=(start_date, end_date))
        ingredient_list = defaultdict(float)

        # Define unit conversions
        unit_conversions = {'kg': 1000, 'gr': 1, 'lt': 1000, 'cp': 240, 'tablespoon': 15, 'teaspoon': 5, 'ml': 1}

        for meal in meals:
            for dish in meal.dish_set.all():
                recipe = dish.recipe
                portions = dish.portions

                for ingredient_amount in recipe.ingredientamount_set.all():
                    ingredient = ingredient_amount.ingredient
                    amount = ingredient_amount.amount / recipe.portions * portions

                    # Convert to a common unit (ml or g)
                    if ingredient_amount.unit in unit_conversions:
                        amount *= unit_conversions[ingredient_amount.unit]
                        unit = 'ml' if ingredient_amount.unit in ['lt', 'cp', 'tbl', 'tsp'] else 'gr'
                    else:
                        unit = ingredient_amount.unit

                    # Convert the tuple key to a string
                    ingredient_key = f"{ingredient.name}, {unit}"

                    # Add to the total ingredient list
                    ingredient_list[ingredient_key] += amount

        return dict(ingredient_list)


class Dish(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    portions = models.IntegerField(blank=False, null=False, default=1)


class ExtraItems(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    item = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    UNITS_CHOICES = [
        ('gr', 'grams'),
        ('kg', 'kilograms'),
        ('ml', 'milliliters'),
        ('lt', 'liters'),
        ('unt', 'units'),
        ('cl', 'cloves'),
        ('tsp', 'teaspoon'),
        ('cp', 'cup'),
        ('tbl', 'tablespoon')
        # TODO add spoons, cups etc
    ]
    unit = models.CharField(max_length=3, choices=UNITS_CHOICES)
    amount = models.FloatField(blank=False, null=False)
