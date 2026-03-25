from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import Libro, Categoria, Pedido, ItemPedido, Cliente
from .forms import PedidoForm, RegistroClienteForm


def catalogo(request):
    libros = Libro.objects.filter(disponible=True, stock__gt=0).select_related('categoria')
    categorias = Categoria.objects.all()
    cat_id = request.GET.get('categoria')
    q = request.GET.get('q', '')
    if cat_id:
        libros = libros.filter(categoria_id=cat_id)
    if q:
        libros = libros.filter(titulo__icontains=q) | libros.filter(autor__icontains=q)
    carrito = request.session.get('carrito', {})
    return render(request, 'libreria/tienda/catalogo.html', {
        'libros': libros, 'categorias': categorias,
        'cat_sel': cat_id, 'q': q,
        'total_carrito': sum(v['cantidad'] for v in carrito.values()),
    })


def libro_detalle(request, pk):
    libro = get_object_or_404(Libro, pk=pk, disponible=True)
    carrito = request.session.get('carrito', {})
    return render(request, 'libreria/tienda/libro_detalle.html', {
        'libro': libro,
        'total_carrito': sum(v['cantidad'] for v in carrito.values()),
    })


def agregar_carrito(request, pk):
    libro = get_object_or_404(Libro, pk=pk, disponible=True)
    carrito = request.session.get('carrito', {})
    key = str(pk)
    cantidad = int(request.POST.get('cantidad', 1))
    if key in carrito:
        nueva_cant = carrito[key]['cantidad'] + cantidad
        if nueva_cant > libro.stock:
            messages.warning(request, f'Solo hay {libro.stock} unidades disponibles.')
            nueva_cant = libro.stock
        carrito[key]['cantidad'] = nueva_cant
    else:
        carrito[key] = {
            'titulo': libro.titulo,
            'precio': str(libro.precio),
            'cantidad': min(cantidad, libro.stock),
            'imagen': libro.imagen if libro.imagen else '',
        }
    request.session['carrito'] = carrito
    messages.success(request, f'"{libro.titulo}" agregado al carrito.')
    return redirect('tienda_catalogo')


def quitar_carrito(request, pk):
    carrito = request.session.get('carrito', {})
    carrito.pop(str(pk), None)
    request.session['carrito'] = carrito
    return redirect('tienda_carrito')


def actualizar_carrito(request, pk):
    """Actualiza la cantidad de un libro en el carrito."""
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        key = str(pk)
        if key in carrito:
            try:
                nueva_cant = int(request.POST.get('cantidad', 1))
                libro = get_object_or_404(Libro, pk=pk)
                if nueva_cant < 1:
                    nueva_cant = 1
                if nueva_cant > libro.stock:
                    messages.warning(request, f'Solo hay {libro.stock} unidades disponibles.')
                    nueva_cant = libro.stock
                carrito[key]['cantidad'] = nueva_cant
                request.session['carrito'] = carrito
                messages.success(request, 'Cantidad actualizada.')
            except (ValueError, TypeError):
                messages.error(request, 'Cantidad inválida.')
    return redirect('tienda_carrito')


def carrito(request):
    carrito = request.session.get('carrito', {})
    items = []
    total = 0
    for pk, datos in carrito.items():
        subtotal = float(datos['precio']) * datos['cantidad']
        total += subtotal
        items.append({**datos, 'pk': pk, 'subtotal': subtotal})
    return render(request, 'libreria/tienda/carrito.html', {
        'items': items, 'total': total,
        'total_carrito': sum(v['cantidad'] for v in carrito.values()),
    })


@login_required(login_url='/login/')
def checkout(request):
    carrito_session = request.session.get('carrito', {})
    if not carrito_session:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('tienda_catalogo')

    try:
        cliente = request.user.cliente
    except Exception:
        messages.error(request, 'No tienes perfil de cliente. Regístrate correctamente.')
        return redirect('tienda_registro')

    form = PedidoForm(request.POST or None)
    if form.is_valid():
        pedido = form.save(commit=False)
        pedido.cliente = cliente
        pedido.save()
        total = Decimal('0')
        for pk, datos in carrito_session.items():
            libro = get_object_or_404(Libro, pk=int(pk))
            precio = Decimal(str(datos['precio']))
            item = ItemPedido(
                pedido=pedido,
                libro=libro,
                cantidad=datos['cantidad'],
                precio_unitario=precio,
            )
            item.save()
            total += precio * datos['cantidad']
        pedido.calcular_total()
        request.session['carrito'] = {}
        messages.success(request, f'¡Pedido #{pedido.pk} registrado exitosamente!')
        return redirect('tienda_mis_pedidos')

    items = []
    total = 0
    for pk, datos in carrito_session.items():
        subtotal = float(datos['precio']) * datos['cantidad']
        total += subtotal
        items.append({**datos, 'pk': pk, 'subtotal': subtotal})

    return render(request, 'libreria/tienda/checkout.html', {
        'form': form, 'items': items, 'total': total,
        'total_carrito': sum(v['cantidad'] for v in carrito_session.values()),
    })


@login_required(login_url='/login/')
def mis_pedidos(request):
    try:
        cliente = request.user.cliente
        pedidos = Pedido.objects.filter(cliente=cliente).prefetch_related('items__libro')
    except Exception:
        pedidos = []
    return render(request, 'libreria/tienda/mis_pedidos.html', {
        'pedidos': pedidos,
        'total_carrito': 0,
    })


def registro(request):
    form = RegistroClienteForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, '¡Cuenta creada! Bienvenido a la librería.')
        return redirect('tienda_catalogo')
    return render(request, 'libreria/tienda/registro.html', {'form': form})