# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Crée un routeur pour gérer les routes REST standard
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('users/me/', UserViewSet.as_view({'delete': 'destroy_self'}), name='user-delete-self'),
    path('', include(router.urls)),  # Inclure les autres routes
]
