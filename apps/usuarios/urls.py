# =================================================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuariosView

# =================================================================================

router = DefaultRouter()
router.register('', UsuariosView, basename='usuarios')

urlpatterns = [
    path('', include(router.urls)),
]

# =================================================================================
