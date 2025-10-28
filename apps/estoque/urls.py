# =================================================================================

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PecasView, CSVView

# =================================================================================

router = DefaultRouter() # Cria um roteador padrão do DRF (Get, Post, Put, Delete)
router.register(r'pecas', PecasView, basename='pecas')

urlpatterns = [
    path('pecas/upload-csv/', CSVView.as_view(), name='upload_csv'),
    path('', include(router.urls))

]

# =================================================================================
