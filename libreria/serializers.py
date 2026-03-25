from rest_framework import serializers
from .models import Libro, Cliente, Venta


def validate_campo(value, nombre_campo, tipo='str', min_val=None, max_val=None):
    """Función reutilizable de validación de campos."""
    if tipo == 'str':
        if not value or not str(value).strip():
            raise serializers.ValidationError(f'El campo {nombre_campo} no puede estar vacío.')
    elif tipo == 'num':
        if value is None:
            raise serializers.ValidationError(f'El campo {nombre_campo} es obligatorio.')
        if min_val is not None and value < min_val:
            raise serializers.ValidationError(f'{nombre_campo} debe ser mayor o igual a {min_val}.')
        if max_val is not None and value > max_val:
            raise serializers.ValidationError(f'{nombre_campo} debe ser menor o igual a {max_val}.')
    return value


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
        read_only_fields = ['stock_bajo', 'creado_en', 'actualizado_en']

    def validate_titulo(self, value):
        return validate_campo(value, 'título', tipo='str')

    def validate_autor(self, value):
        return validate_campo(value, 'autor', tipo='str')

    def validate_isbn(self, value):
        return validate_campo(value, 'ISBN', tipo='str')

    def validate_precio(self, value):
        return validate_campo(value, 'precio', tipo='num', min_val=0)

    def validate_stock(self, value):
        return validate_campo(value, 'stock', tipo='num', min_val=0)


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
        read_only_fields = ['creado_en']

    def validate_nombre(self, value):
        return validate_campo(value, 'nombre', tipo='str')

    def validate_email(self, value):
        return validate_campo(value, 'email', tipo='str')


class VentaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    libro_titulo = serializers.CharField(source='libro.titulo', read_only=True)

    class Meta:
        model = Venta
        fields = '__all__'
        read_only_fields = ['precio_unitario', 'total', 'fecha', 'cliente_nombre', 'libro_titulo']

    def validate_cantidad(self, value):
        return validate_campo(value, 'cantidad', tipo='num', min_val=1)

    def validate(self, data):
        libro = data.get('libro')
        cantidad = data.get('cantidad', 0)
        if libro and libro.stock < cantidad:
            raise serializers.ValidationError(
                f'Stock insuficiente. Disponible: {libro.stock}, solicitado: {cantidad}'
            )
        return data
