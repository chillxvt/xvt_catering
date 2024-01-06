from django.urls import path
from django.urls import re_path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('', views.api_welcome),
    path('register/', views.register),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('recipes/add/', views.add_recipe),
    path('recipes/get/<int:pk>/', views.get_recipe),
    path('recipes/update/<int:pk>/', views.update_recipe),
    path('recipes/delete/<int:pk>/', views.delete_recipe),
    path('ingredients/add/', views.add_ingredient),
    path('ingredients/get/<int:pk>/', views.get_ingredient),
    path('ingredients/update/<int:pk>/', views.update_ingredient),
    path('ingredients/delete/<int:pk>/', views.delete_ingredient),
    path('meals/add/', views.add_meal),
    path('meals/get/<int:pk>/', views.get_meal),
    # path('meals/update/<int:pk>/', views.update_meal),
    # path('meals/delete/<int:pk>/', views.delete_meal),
    path('meals/get_range/<str:start_date>/<str:end_date>/', views.get_meals_between_dates),
    path('meals/get_shopping_list/<str:start_str>/<str:end_str>/', views.ingredient_list)
]
