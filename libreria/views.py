from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Libro, Cliente, Venta
from .serializers import LibroSerializer, ClienteSerializer, VentaSerializer


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all().order_by('-creado_en')
    serializer_class = LibroSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='stock-bajo')
    def stock_bajo(self, request):
        libros = Libro.objects.filter(stock_bajo=True)
        serializer = self.get_serializer(libros, many=True)
        return Response(serializer.data)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('-creado_en')
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]


class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.select_related('cliente', 'libro').order_by('-fecha')
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']  # ventas no se editan
