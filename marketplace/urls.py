
# =================================================================================

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# =================================================================================

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Apps
    path('api/estoque/', include('apps.estoque.urls')),  # sem namespace
    path('api/usuarios/', include('apps.usuarios.urls')),  # sem namespace
]

# =================================================================================
