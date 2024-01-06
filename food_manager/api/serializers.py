from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from food_manager.models import Ingredient, Recipe, IngredientAmount, Meal, Dish, ExtraItems
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = get_user_model()
        fields = ['username', 'password', 'email']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class IngredientAmountSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = IngredientAmount
        fields = ['id', 'ingredient', 'unit', 'amount']

    def create(self, validated_data):
        ingredient_data = validated_data.pop('ingredient', {})
        ingredient_instance, created = Ingredient.objects.get_or_create(**ingredient_data)

        # Use `recipe` from the context (assuming it's available in the serializer context)
        recipe = self.context.get('recipe')

        # Create IngredientAmount with proper association to Recipe and Ingredient
        ingredient_amount_instance = IngredientAmount.objects.create(recipe=recipe, ingredient=ingredient_instance,
                                                                     **validated_data)

        return ingredient_amount_instance

    def update(self, instance, validated_data):
        ingredient_data = validated_data.pop('ingredient', {})
        ingredient_instance, created = Ingredient.objects.get_or_create(**ingredient_data)

        instance.ingredient = ingredient_instance
        instance.unit = validated_data.get('unit', instance.unit)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()

        return instance


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientAmountSerializer(many=True, write_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'instructions', 'ingredients', 'portions']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])

        # Create or update the recipe based on its name
        recipe_instance, created = Recipe.objects.get_or_create(
            name=validated_data['name'],
            defaults={
                'instructions': validated_data.get('instructions', ''),
                'portions': validated_data.get('portions', 1)  # Default value for portions
            }
        )

        # Create or update each ingredient and its amount
        for ia_data in ingredients_data:
            ingredient_data = ia_data.pop('ingredient', {})
            ingredient_instance, created = Ingredient.objects.get_or_create(**ingredient_data)
            IngredientAmount.objects.create(recipe=recipe_instance, ingredient=ingredient_instance, **ia_data)

        # Serialize the recipe along with its ingredients
        serializer = RecipeSerializer(recipe_instance, context=self.context)
        return serializer.data

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.portions = validated_data.get('portions', instance.portions)
        instance.save()

        ingredients_data = validated_data.get('ingredients', [])

        # Update or create IngredientAmount instances
        for ia_data in ingredients_data:
            ingredient_data = ia_data.get('ingredient', {})
            ingredient_name = ingredient_data.get('name')

            # Check if ingredient name is provided
            if ingredient_name:
                ingredient, created = Ingredient.objects.get_or_create(name=ingredient_name)

                ia_instance, ia_created = IngredientAmount.objects.update_or_create(
                    recipe=instance,
                    ingredient=ingredient,
                    defaults={'unit': ia_data.get('unit', ''), 'amount': ia_data.get('amount', 0)}
                )
            else:
                # Handle the case where ingredient name is not provided
                ia_instance = None

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if the ingredientamount_set attribute exists
        if hasattr(instance, 'ingredientamount_set'):
            # Include ingredients in the serialized data
            representation['ingredients'] = IngredientAmountSerializer(instance.ingredientamount_set.all(),
                                                                       many=True).data
        elif 'ingredients' in representation:
            # For creation, include ingredients from validated_data
            representation['ingredients'] = representation.get('ingredients', [])
        else:
            # For retrieval, exclude ingredients field
            representation.pop('ingredients', None)

        return representation

    # TODO Serializer works correctly with a GET reqest to the server, returns full JSON information.
    # However, Response to a successful POST doesn't carry the full recipe information. Does it need to?


class DishSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer()  # Use RecipeSerializer for the nested recipe field

    class Meta:
        model = Dish
        fields = ['id', 'recipe', 'portions']

    def create(self, validated_data):
        recipe_data = validated_data.pop('recipe', {})
        ingredients_data = recipe_data.pop('ingredients', [])

        if 'name' in recipe_data and not any(recipe_data.values()):
            recipe_instance = Recipe.objects.get_or_404(name=recipe_data['name'])
        else:
            # Create or update the associated recipe
            recipe_instance, created = Recipe.objects.get_or_create(**recipe_data)

        # Create or update each ingredient and its amount
        for ia_data in ingredients_data:
            ingredient_data = ia_data.pop('ingredient', {})
            ingredient_instance, created = Ingredient.objects.update_or_create(**ingredient_data)
            IngredientAmount.objects.get_or_create(recipe=recipe_instance, ingredient=ingredient_instance, **ia_data)

        validated_data['recipe'] = recipe_instance
        return Dish.objects.create(**validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if the recipe attribute exists
        if hasattr(instance, 'recipe'):
            # Include ingredients in the serialized data
            representation['recipe'] = RecipeSerializer(instance.recipe).data

        return representation


class ExtraItemsSerializer(serializers.ModelSerializer):
    item = IngredientSerializer()

    class Meta:
        model = ExtraItems
        fields = ['id', 'item', 'unit', 'amount']

    def create(self, validated_data):
        item_data = validated_data.pop('item', {})
        item_instance, created = Ingredient.objects.get_or_create(**item_data)

        return ExtraItems.objects.create(item=item_instance, **validated_data)

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item', {})
        item_instance, created = Ingredient.objects.get_or_create(**item_data)

        instance.item = item_instance
        instance.unit = validated_data.get('unit', instance.unit)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()

        return instance


class MealSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, write_only=True)
    extras = ExtraItemsSerializer(many=True, write_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'date', 'meal', 'dishes', 'extras']

    def is_valid(self, raise_exception=False):
        print("Entering is_valid method of MealSerializer")

        for field_name, field in self.fields.items():
            try:
                value = self.initial_data[field_name]
                print(f"Field: {field_name}, Value: {value}")
            except KeyError:
                pass

        result = super().is_valid(raise_exception=raise_exception)
        print(f"Validation result: {result}")
        print("Exiting is_valid method of MealSerializer")
        return result

    def validate(self, data):
        print("Entering validate method of MealSerializer")
        validated_data = super().validate(data)
        print("Exiting validate method of MealSerializer")
        return validated_data

    def create(self, validated_data):
        print("Entering create method of MealSerializer")
        dishes_data = validated_data.pop('dishes', [])
        extras_data = validated_data.pop('extras', [])

        # Create the meal instance
        meal = Meal.objects.create(**validated_data)
        print("Meal instance created:", meal.id)

        try:
            # Create or update the Dish instances
            for dish_data in dishes_data:
                print("Processing dish_data:", dish_data)
                recipe_data = dish_data.get('recipe', {})
                if 'name' in recipe_data and not any(recipe_data.values()):
                    # Reference existing recipe by name if available
                    recipe_instance = Recipe.objects.get(name=recipe_data['name'])
                else:
                    # Create or update the associated recipe
                    recipe_instance, created = Recipe.objects.update_or_create(name=recipe_data.get('name', ''),
                                                                                defaults={'instructions': recipe_data.get('instructions', ''),
                                                                                          'portions': recipe_data.get('portions', 1)})
                print("Recipe instance created or updated:", recipe_instance.id)

                dish_data['meal'] = meal
                dish_data['recipe'] = recipe_instance

                # Create or update Dish instance with proper association to Recipe and Meal
                dish_instance, created = Dish.objects.update_or_create(
                    meal=meal,
                    recipe=recipe_instance,
                    defaults={'portions': dish_data.get('portions', 1)}  # Default value for portions
                )
                print("Dish instance created or updated:", dish_instance.id)
        except Exception as dish_error:
            print(f"Error creating Dish: {dish_error}")

        try:
            # Create or update the ExtraItems instances
            for extra_data in extras_data:
                print("Processing extra_data:", extra_data)
                item_data = extra_data.get('item', {})
                item_instance, created = Ingredient.objects.update_or_create(**item_data)
                extra_item_instance, created = ExtraItems.objects.create(meal=meal, item=item_instance, **extra_data)
                print("ExtraItems instance created:", extra_item_instance.id)
        except Exception as extras_error:
            print(f"Error creating ExtraItems: {extras_error}")

        print("Exiting create method of MealSerializer")
        return meal

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if the dish_set and extraitems_set attributes exist
        if hasattr(instance, 'dish_set'):
            # Include dishes in the serialized data
            representation['dishes'] = DishSerializer(instance.dish_set.all(), many=True).data

        if hasattr(instance, 'extraitems_set'):
            # Include extras in the serialized data
            representation['extras'] = ExtraItemsSerializer(instance.extraitems_set.all(), many=True).data

        return representation