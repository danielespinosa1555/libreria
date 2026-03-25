# 📚 Sistema de Librería — Grupo 3

**Integrantes:**
- Diaz Espinosa Daniel Felipe
- Forero Ruiz Sara Nicol
- Sanchez Rivera Juan Sebastian

---

## 📋 Descripción

Sistema de gestión de inventario y ventas para una librería independiente, desarrollado con Django + Django REST Framework + Supabase (PostgreSQL).

## 🗂 Modelos

| Modelo   | Descripción                          |
|----------|--------------------------------------|
| `Libro`  | Inventario de libros con stock       |
| `Cliente`| Compradores registrados              |
| `Venta`  | Registro de ventas con descuento automático de stock |

## ⚙️ Regla de Negocio

Al crear una venta:
1. Se descuenta automáticamente el stock del libro.
2. Si el stock queda **menor a 3**, el campo `stock_bajo` se marca como `True`.

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd libreria_proyecto

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales de Supabase

# 5. Aplicar migraciones
python manage.py migrate

# 6. Crear superusuario
python manage.py createsuperuser

# 7. Correr el servidor
python manage.py runserver
```

## 🔑 Autenticación con Token

```bash
# Obtener token
POST /api/token/
Body: { "username": "admin", "password": "tu_password" }

# Usar token en requests
Headers: Authorization: Token <tu_token>
```

## 🌐 Endpoints API

| Método | Endpoint                    | Descripción              |
|--------|-----------------------------|--------------------------|
| GET    | `/api/libros/`              | Listar libros            |
| POST   | `/api/libros/`              | Crear libro              |
| GET    | `/api/libros/{id}/`         | Detalle libro            |
| PUT    | `/api/libros/{id}/`         | Actualizar libro         |
| DELETE | `/api/libros/{id}/`         | Eliminar libro           |
| GET    | `/api/libros/stock-bajo/`   | Libros con stock bajo    |
| GET    | `/api/clientes/`            | Listar clientes          |
| POST   | `/api/clientes/`            | Crear cliente            |
| GET    | `/api/ventas/`              | Listar ventas            |
| POST   | `/api/ventas/`              | Registrar venta          |

## 🖥 Vistas HTML

| Ruta                         | Descripción           |
|------------------------------|-----------------------|
| `/`                          | Lista de libros       |
| `/libros/nuevo/`             | Crear libro           |
| `/clientes/`                 | Lista de clientes     |
| `/ventas/`                   | Lista de ventas       |

## 🗄 Base de Datos

Configurado para **Supabase (PostgreSQL)**. Configura las variables `DB_*` en tu archivo `.env`.
