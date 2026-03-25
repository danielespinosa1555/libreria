from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Libro, Cliente, Venta, Categoria, Pedido, ItemPedido


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'precio', 'stock', 'stock_bajo', 'disponible']
    list_filter = ['stock_bajo', 'disponible', 'categoria']
    search_fields = ['titulo', 'autor', 'isbn']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono', 'creado_en']
    search_fields = ['nombre', 'email']


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cliente', 'libro', 'cantidad', 'total', 'fecha']
    readonly_fields = ['precio_unitario', 'total', 'fecha']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cliente', 'estado', 'tipo_envio', 'total', 'creado_en']
    list_filter = ['estado', 'tipo_envio']
    inlines = [ItemPedidoInline]


# ✅ Personaliza el admin de Usuario para mostrar el rol claramente
class TrabajadorAdmin(UserAdmin):
    # Columnas visibles en la lista
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active']

    def rol(self, obj):
        if obj.is_superuser:
            return '👑 Admin'
        elif obj.is_staff:
            return '🔧 Trabajador'
        else:
            return '🛒 Cliente'
    rol.short_description = 'Rol'

    # Al CREAR un usuario, muestra el campo is_staff para asignar rol
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Rol', {
            'classes': ('wide',),
            'fields': ('is_staff', 'is_superuser'),
            'description': 'Marcar "is_staff" para crear un Trabajador.',
        }),
    )


# Reemplaza el UserAdmin por defecto con el personalizado
admin.site.unregister(User)
admin.site.register(User, TrabajadorAdmin)