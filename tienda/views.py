from django import forms
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from carro.carro import Carro
from .serializers import *
from .models import *
from .forms import *
import requests
import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Producto
from io import *

# API Dolar
class Mindicador:
 
    def __init__(self, indicador, year):
        self.indicador = indicador
        self.year = year
    
    def InfoApi(self):
        # En este caso hacemos la solicitud para el caso de consulta de un indicador en un año determinado
        url = f'https://mindicador.cl/api/{self.indicador}/{self.year}'
        response = requests.get(url)
        data = json.loads(response.text.encode("utf-8"))
        # Para que el json se vea ordenado, retornar pretty_json
        pretty_json = json.dumps(data, indent=2)
        return data

# Viewset para manejar solicitudes tipo HTTP (GET, POST, PUT, DELETE)
class EmpleadoViewSet(viewsets.ModelViewSet):
    queryset = Empleado.objects.all().order_by('id')
    serializer_class = EmpleadoSerializers
    renderer_classes = [JSONRenderer]

class ServicioViewSet(viewsets.ModelViewSet):
    queryset = Servicio.objects.all().order_by('id')
    serializer_class = ServicioSerializers
    renderer_classes = [JSONRenderer]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('id')
    serializer_class = ProductoSerializers
    renderer_classes = [JSONRenderer]

# Métodos para listar desde API.
def empleadosapi(request):
    response = requests.get('http://127.0.0.1:8000/api/empleados/')
    empleados = response.json()

    aux = {
        'lista' : empleados
    }

    return render(request, 'tienda/empleados/crudapi/index.html', aux)

def serviciosapi(request):
    response = requests.get(f'http://127.0.0.1:8000/api/servicios/')
    servicios = response.json()

    aux = {
        'lista' : servicios
    }

    return render(request, 'tienda/servicios/crudapi/index.html', aux)

def productosapi(request):
    response = requests.get('http://127.0.0.1:8000/api/productos/')
    productos = response.json()

    paginator = Paginator(productos, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    aux = {
        'page_obj': page_obj
    }

    return render(request, 'tienda/productos/crudapi/index.html', aux)

# Inicio
def index(request):
    productos = Producto.objects.all()

    return render(request, 'index.html', {'productos': productos})

def nosotros(request):
    return render(request, 'nosotros.html', {})

# Login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Carrito
            current_user = Perfil.objects.get(usuario__id=request.user.id)
            # Obtener carrito
            carro_guardado = current_user.carrito_viejo
            # Convertir
            if carro_guardado:
                carro_convertido = json.loads(carro_guardado)
                # añadir carrito
                carro = Carro(request)

                for key, value in carro_convertido.items():
                    carro.db_agregar(producto=key, cantidad=value)

            messages.success(request, ("Has iniciado sesión."))
            return redirect('index')
        else:
            messages.success(request, ("Ha ocurrido un error, intenta nuevamente."))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Has cerrado la sesión."))
    return redirect('index')

# Registro
def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Logea
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registrado! Rellena tus datos!"))
            return redirect('actualizar_info')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            messages.success(request, ("Ha ocurrido un error, intenta nuevamente."))
            return redirect('register')

    return render(request, 'register.html', {'form': form})

# Usuario
def actualizar_usuario(request):
    if request.user.is_authenticated:
        usuario_actual = User.objects.get(id=request.user.id)
        form_usuario = UpdateUserForm(request.POST or None, instance = usuario_actual)

        if form_usuario.is_valid():
            form_usuario.save()

            login(request, usuario_actual)
            messages.success(request, "Usuario ha sido actualizado!")
            return redirect('index')
        return render(request, 'actualizar_usuario.html', {'form_usuario': form_usuario})
    else:
        messages.success(request, "Debes iniciar sesión para acceder a esa página.")
        return redirect('index')

def actualizar_info(request):
    if request.user.is_authenticated:
        usuario_actual = Perfil.objects.get(usuario__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance = usuario_actual)

        if form.is_valid():
            form.save()
            messages.success(request, "Tú informacion ha sido actualizada!")
            return redirect('index')
        return render(request, 'actualizar_info.html', {'form': form})
    else:
        messages.success(request, "Debes iniciar sesión para acceder a esa página.")
        return redirect('index')
    
def account_locked(request):
    return render(request, 'account_locked.html')

# Empleado
def empleados(request):
    empleados = Empleado.objects.all() # SELECT * FROM empleado

    aux = {
        'lista' : empleados
    }

    return render(request, 'tienda/empleados/index.html', aux)

@permission_required('tienda.add_empleado')
def empleadosadd(request):
    aux = {
            'form' : EmpleadoForm()
    }

    if request.method == 'POST':
        formulario = EmpleadoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['msj'] = 'Empleado almacenado correctamente!'
            messages.success(request, ("El empleado se ha creado exitosamente!"))
            return redirect('empleados')
        else:
            aux['form'] = formulario
            messages.success(request, ("Ha ocurrido un error al crear Empleado, vuelva a intentarlo"))

    return render(request, 'tienda/empleados/crud/add.html', aux)

def empleadosupdate(request, id):
    empleado = Empleado.objects.get(id=id)
    aux = {
            'form' : EmpleadoForm(instance = empleado)
    }

    if request.method == 'POST':
        formulario = EmpleadoForm(data = request.POST, instance = empleado, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            aux['msj'] = 'Empleado modificado correctamente!'
            messages.success(request, ("El empleado se ha modificado exitosamente!"))
            return redirect('empleados')
        else:
            aux['form'] = formulario
            messages.success(request, ("Ha ocurrido un error al modificar Empleado, vuelva a intentarlo"))

    return render(request, 'tienda/empleados/crud/update.html', aux)

@permission_required('tienda.delete_empleado')
def empleadosdelete(request, id):
    empleado = Empleado.objects.get(id=id)
    empleado.delete()

    messages.success(request, ("El empleado se ha eliminado exitosamente!"))
    return redirect(to="empleados")

# Producto
def producto_id(request, pk):
    producto = Producto.objects.get(id=pk)
    return render(request, 'producto.html', {'producto': producto})

def productos(request):
    productos = Producto.objects.all()

    aux = {
        'lista': productos
    }

    return render(request, 'tienda/productos/index.html', aux)

def productosadd(request):
    aux = {
            'form' : ProductoForm()
    }

    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['msj'] = 'Empleado almacenado correctamente!'
            messages.success(request, ("El producto se ha creado exitosamente!"))
            return redirect('productos')
        else:
            print("No valido", formulario.errors)
            aux['form'] = formulario
            messages.success(request, ("El producto no se pudo crear!"))

    indicador = 'dolar'
    year = '2024'
    api = Mindicador(indicador, year)
    datos_api = api.InfoApi()

    serie = datos_api.get('serie', [])
    primer_item = serie[0] if serie else None
    valor_api = primer_item.get('valor', 10) if primer_item else 10

    aux['form'] = ProductoForm(initial={'precio_base': valor_api})

    return render(request, 'tienda/productos/crud/add.html', aux)

@permission_required('core.change_servicio')
def productosupdate(request, id):
    producto = Producto.objects.get(id=id)
    aux = {
            'form' : ProductoForm(instance = producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data = request.POST, instance = producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            aux['msj'] = 'Servicio modificado correctamente!'
            messages.success(request, ("El producto se ha modificado exitosamente!"))
            return redirect('productos')
        else:
            aux['form'] = formulario
            messages.success(request, ("El producto no se pudo modificar!"))
            aux['msj'] = 'No se pudo modificar :('

    return render(request, 'tienda/productos/crud/update.html', aux)

@permission_required('core.delete_servicio')
def productosdelete(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()

    messages.success(request, ("El producto se ha eliminado exitosamente!"))
    return redirect(to="productos")

# Compras
def historial_compras(request):
    compras = Compra.objects.filter(usuario=request.user).order_by('-fecha_compra')
    return render(request, 'historial_compras.html', {'compras': compras})

# Servicio
def servicios(request):
    servicios = Servicio.objects.all()

    aux = {
        'lista' : servicios
    }

    return render(request, 'tienda/servicios/index.html', aux)

@login_required
def serviciosadd(request):
    aux = {
            'form' : ServicioForm()
    }

    if request.method == 'POST':
        formulario = ServicioForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['msj'] = 'Empleado almacenado correctamente!'
            messages.success(request, ("El servicio se ha creado exitosamente!"))
            return redirect('servicios')
        else:
            aux['form'] = formulario
            aux['msj'] = 'No se pudo almacenar :('

    return render(request, 'tienda/servicios/crud/add.html', aux)

@permission_required('core.change_servicio')
def serviciosupdate(request, id):
    servicio = Servicio.objects.get(id=id)
    aux = {
            'form' : ServicioForm(instance = servicio)
    }

    if request.method == 'POST':
        formulario = ServicioForm(data = request.POST, instance = servicio, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            aux['form'] = formulario
            aux['msj'] = 'Servicio modificado correctamente!'
            messages.success(request, ("El servicio se ha modificado exitosamente!"))
            return redirect('servicios')
        else:
            aux['form'] = formulario
            aux['msj'] = 'No se pudo modificar :('

    return render(request, 'tienda/servicios/crud/update.html', aux)

@permission_required('core.delete_servicio')
def serviciosdelete(request, id):
    servicio = Servicio.objects.get(id=id)
    servicio.delete()

    messages.success(request, ("El servicio se ha eliminado exitosamente!"))
    return redirect(to="servicios")

# Categoria
def categoria(request, foo):
    foo = foo.replace('-', ' ')
    try:
        categoria = Categoria.objects.get(nombre=foo)
        productos = Producto.objects.filter(categoria=categoria)
        return render(request, 'categoria.html', {'productos': productos, 'categoria': categoria})
    except Categoria.DoesNotExist:
        messages.success(request, ("La categoria no existe."))
        return redirect('index')
    except Exception as e:
        messages.error(request, f"Error inesperado: {e}")
        return redirect('index')