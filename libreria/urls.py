from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LibroViewSet, ClienteViewSet, VentaViewSet

router = DefaultRouter()
router.register(r'libros', LibroViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'ventas', VentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
