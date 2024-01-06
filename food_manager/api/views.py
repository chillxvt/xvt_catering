from django.contrib.auth import get_user_model
from food_manager.models import Ingredient, Recipe, Meal
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.response import Response
from food_manager.api.serializers import *
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from collections import defaultdict
from django.db import IntegrityError


# Create your views here.

# User registration view

@api_view(['GET'])
def api_welcome(request):
    return Response({"detail": "Welcome to XVT catering app!"
                               " Please register via /api/register"
                               " or get your tokens via /api/token!"})


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user, created = get_user_model().objects.get_or_create(username=request.data["username"],
                                                               defaults=serializer.validated_data)
        if not created:
            return Response({"error": "User already exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        user.set_password(raw_password=request.data["password"])
        user.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# ingredient views (TODO maybe convert to class-based)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    serializer = IngredientSerializer(ingredient)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_ingredient(request):
    serializer = IngredientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO add validation somewhere that makes sure that names aren't too similar


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    serializer = IngredientSerializer(instance=ingredient, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    ingredient.delete()
    return Response({"message": "Ingredient deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# recipe views (TODO maybe convert to class based)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data, status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_recipe(request):
    print(request.data)
    serializer = RecipeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({'id': serializer.data['id']}, status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO add validation somewhere that makes sure that names aren't too similar


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    serializer = RecipeSerializer(instance=recipe, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.delete()
    return Response({"message": "Recipe deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# meal views

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_meal(request):
    try:
        # Attempt to create a new meal
        serializer = MealSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"id": serializer.data['id']}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            # Handle the case where the unique constraint is violated
            return Response({'error': 'You can not plan meals for the same time, or overwrite existing recipes!'},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle other IntegrityError cases
            return Response({'error': 'An error occurred while saving the meal.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meal(request, pk):
    # Retrieve the Meal instance or return 404 if not found
    meal = get_object_or_404(Meal, pk=pk, user=request.user)

    # Serialize the Meal instance
    serializer = MealSerializer(meal)

    # Return the serialized data in the response
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_meals_between_dates(request, start_date, end_date):
    try:
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return Response({"detail": "Invalid date format. Please use YYYY-MM-DD."}, status.HTTP_400_BAD_REQUEST)

    # Retrieve meals between the given dates for the authenticated user
    meals = Meal.objects.filter(user=request.user, date__range=[start_date, end_date])

    # Serialize the meals
    serializer = MealSerializer(meals, many=True)

    # Return the serialized data in the response
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ingredient_list(request, start_str, end_str):
    if not start_str or not end_str:
        return Response({'error': 'Both start_date and end_date are required'}, status.HTTP_400_BAD_REQUEST)
    try:
        start_date = timezone.datetime.strptime(str(start_str), '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(str(end_str), '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
    try:
        print(start_date, end_date)
        ingredients_list = Meal.extract_ingredient_list(start_date, end_date)

        return Response({'ingredient_list': ingredients_list})

    except ValueError as e:
        return Response({"detail": str(e)}, status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
