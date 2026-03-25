from django.urls import path
from . import views_tienda

urlpatterns = [
    path('', views_tienda.catalogo, name='tienda_catalogo'),
    path('libro/<int:pk>/', views_tienda.libro_detalle, name='tienda_libro_detalle'),
    path('carrito/', views_tienda.carrito, name='tienda_carrito'),
    path('carrito/agregar/<int:pk>/', views_tienda.agregar_carrito, name='tienda_agregar_carrito'),
    path('carrito/quitar/<int:pk>/', views_tienda.quitar_carrito, name='tienda_quitar_carrito'),
    path('carrito/actualizar/<int:pk>/', views_tienda.actualizar_carrito, name='tienda_actualizar_carrito'),  # ✅ nuevo
    path('checkout/', views_tienda.checkout, name='tienda_checkout'),
    path('mis-pedidos/', views_tienda.mis_pedidos, name='tienda_mis_pedidos'),
    path('registro/', views_tienda.registro, name='tienda_registro'),
]