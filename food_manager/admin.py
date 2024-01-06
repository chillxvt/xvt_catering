from django.contrib import admin

# Register your models here.
from .models import Ingredient, Recipe, Meal, IngredientAmount, Dish, ExtraItems


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class DishInline(admin.TabularInline):
    model = Dish
    extra = 1


class ExtraItemsInline(admin.TabularInline):
    model = ExtraItems
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientAmountInline,)


class MealAdmin(admin.ModelAdmin):
    inlines = (DishInline, ExtraItemsInline,)


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Meal, MealAdmin)
