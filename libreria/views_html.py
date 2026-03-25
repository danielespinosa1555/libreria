from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import path
from .models import Libro, Cliente, Venta, Categoria, Pedido, ItemPedido
from .forms import LibroForm, ClienteForm, VentaForm, CategoriaForm, RegistroTrabajadorForm
from .decorators import staff_o_dueno, solo_dueno


@staff_o_dueno
def libro_list(request):
    libros = Libro.objects.select_related('categoria').all()
    categorias = Categoria.objects.all()
    cat_id = request.GET.get('categoria')
    if cat_id:
        libros = libros.filter(categoria_id=cat_id)
    q = request.GET.get('q')
    if q:
        libros = libros.filter(titulo__icontains=q) | libros.filter(autor__icontains=q)
    return render(request, 'libreria/libros.html', {
        'libros': libros, 'categorias': categorias, 'cat_sel': cat_id, 'q': q
    })


@staff_o_dueno
def cliente_list(request):
    clientes = Cliente.objects.all().order_by('-creado_en')
    return render(request, 'libreria/clientes.html', {'clientes': clientes})


@staff_o_dueno
def venta_list(request):
    ventas = Venta.objects.select_related('cliente', 'libro').order_by('-fecha')
    return render(request, 'libreria/ventas.html', {'ventas': ventas})


@staff_o_dueno
def libro_create(request):
    form = LibroForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Libro creado exitosamente.')
        return redirect('libro_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Nuevo Libro'})


@staff_o_dueno
def libro_edit(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    form = LibroForm(request.POST or None, request.FILES or None, instance=libro)
    if form.is_valid():
        form.save()
        messages.success(request, 'Libro actualizado.')
        return redirect('libro_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Editar Libro'})


@solo_dueno
def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'Libro eliminado.')
        return redirect('libro_list')
    return render(request, 'libreria/confirm_delete.html', {'objeto': libro, 'tipo': 'Libro'})


@staff_o_dueno
def cliente_create(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente creado exitosamente.')
        return redirect('cliente_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Nuevo Cliente'})


@staff_o_dueno
def cliente_edit(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente actualizado.')
        return redirect('cliente_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Editar Cliente'})


@solo_dueno
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('cliente_list')
    return render(request, 'libreria/confirm_delete.html', {'objeto': cliente, 'tipo': 'Cliente'})


@staff_o_dueno
def venta_create(request):
    form = VentaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Venta registrada exitosamente.')
        return redirect('venta_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Nueva Venta'})


@solo_dueno
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        messages.success(request, 'Venta eliminada.')
        return redirect('venta_list')
    return render(request, 'libreria/confirm_delete.html', {'objeto': venta, 'tipo': 'Venta'})


@solo_dueno
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'libreria/categorias.html', {'categorias': categorias})


@solo_dueno
def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada.')
        return redirect('categoria_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Nueva Categoría'})


@solo_dueno
def categoria_edit(request, pk):
    cat = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=cat)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('categoria_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Editar Categoría'})


@solo_dueno
def categoria_delete(request, pk):
    cat = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        cat.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('categoria_list')
    return render(request, 'libreria/confirm_delete.html', {'objeto': cat, 'tipo': 'Categoría'})


@solo_dueno
def trabajador_create(request):
    form = RegistroTrabajadorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, f'Trabajador "{form.cleaned_data["username"]}" registrado exitosamente.')
        return redirect('trabajador_list')
    return render(request, 'libreria/form.html', {'form': form, 'titulo': 'Registrar Trabajador'})


@solo_dueno
def trabajador_list(request):
    from django.contrib.auth.models import User
    trabajadores = User.objects.filter(is_staff=True, is_superuser=False).order_by('username')
    return render(request, 'libreria/trabajadores.html', {'trabajadores': trabajadores})


@solo_dueno
def trabajador_delete(request, pk):
    from django.contrib.auth.models import User
    trabajador = get_object_or_404(User, pk=pk, is_staff=True, is_superuser=False)
    if request.method == 'POST':
        trabajador.delete()
        messages.success(request, 'Trabajador eliminado.')
        return redirect('trabajador_list')
    return render(request, 'libreria/confirm_delete.html', {'objeto': trabajador, 'tipo': 'Trabajador'})


@staff_o_dueno
def pedido_list(request):
    pedidos = Pedido.objects.all().prefetch_related('items__libro').select_related('cliente').order_by('-creado_en')
    return render(request, 'libreria/pedidos.html', {'pedidos': pedidos})


@staff_o_dueno
def pedido_confirmar(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)

    if request.method == 'POST':
        if pedido.estado != 'pendiente':
            messages.warning(request, 'Este pedido ya fue procesado.')
            return redirect('pedido_list')

        # ✅ Verificar stock antes de confirmar
        for item in pedido.items.all():
            if item.libro.stock < item.cantidad:
                messages.error(request, f'No se puede confirmar: "{item.libro.titulo}" no tiene stock suficiente. Disponible: {item.libro.stock}')
                return redirect('pedido_list')

        # Crear ventas sin descontar stock (ya se descontó al comprar)
        for item in pedido.items.all():
            venta = Venta(
                cliente=pedido.cliente,
                libro=item.libro,
                cantidad=item.cantidad,
                precio_unitario=item.precio_unitario,
                total=item.subtotal,
            )
            from django.db.models import Model
            Model.save(venta)

        pedido.estado = 'confirmado'
        pedido.save(update_fields=['estado'])
        messages.success(request, f'Pedido #{pedido.pk} confirmado y registrado en ventas.')
        return redirect('pedido_list')

    return redirect('pedido_list')


urlpatterns = [
    path('', libro_list, name='libro_list'),
    path('libros/nuevo/', libro_create, name='libro_create'),
    path('libros/<int:pk>/editar/', libro_edit, name='libro_edit'),
    path('libros/<int:pk>/eliminar/', libro_delete, name='libro_delete'),
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:pk>/editar/', cliente_edit, name='cliente_edit'),
    path('clientes/<int:pk>/eliminar/', cliente_delete, name='cliente_delete'),
    path('ventas/', venta_list, name='venta_list'),
    path('ventas/nueva/', venta_create, name='venta_create'),
    path('ventas/<int:pk>/eliminar/', venta_delete, name='venta_delete'),
    path('categorias/', categoria_list, name='categoria_list'),
    path('categorias/nueva/', categoria_create, name='categoria_create'),
    path('categorias/<int:pk>/editar/', categoria_edit, name='categoria_edit'),
    path('categorias/<int:pk>/eliminar/', categoria_delete, name='categoria_delete'),
    path('trabajadores/', trabajador_list, name='trabajador_list'),
    path('trabajadores/nuevo/', trabajador_create, name='trabajador_create'),
    path('trabajadores/<int:pk>/eliminar/', trabajador_delete, name='trabajador_delete'),
    path('pedidos/', pedido_list, name='pedido_list'),
    path('pedidos/<int:pk>/confirmar/', pedido_confirmar, name='pedido_confirmar'),
]