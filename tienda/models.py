from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime
import requests
import json

# API
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

# Empleado
class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=150)
    email = models.CharField(max_length=150, blank= True)
    imagen = models.ImageField(upload_to='uploads/empleado/', null=True, blank=True)

    def __str__(self):
        return self.nombre

# Cliente
class Cliente(models.Model):
    p_nombre = models.CharField(max_length=50)
    s_nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.p_nombre} {self.s_nombre}'
    
    class Meta:
        verbose_name_plural = 'Clientes'

# Perfiles
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    direccion_dos = models.CharField(max_length=200, blank=True)
    ciudad = models.CharField(max_length=200, blank=True)
    comuna = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    pais = models.CharField(max_length=200, blank=True)
    carrito_viejo = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.usuario.username
    
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        user_profile = Perfil(usuario=instance)
        user_profile.save()

post_save.connect(crear_perfil, sender=User)


# Categoria de productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = 'Categorias'

# Producto
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    multiplicador = models.PositiveIntegerField(default=1)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, default=0)    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default=1)
    descripcion = models.CharField(max_length=250, default='', blank=True, null= True)
    imagen = models.ImageField(upload_to='uploads/product/')

    # En Oferta
    is_oferta = models.BooleanField(default=False)
    oferta_precio = models.DecimalField(default=0, decimal_places=2, max_digits=6)

    def save(self, *args, **kwargs):
        # Calcular el precio final antes de guardar
        self.precio_final = round(self.precio_base * self.multiplicador)

        super(Producto, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre    
    
    class Meta:
        verbose_name_plural = 'Productos'

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='CompraProducto')
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_compra = models.DateTimeField(auto_now_add=True)

class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

# Servicio
class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=200)
    descripcion_servicio = models.TextField(max_length=550)
    imagen_servicio = models.ImageField(upload_to='uploads/servicio/', null=True, blank=True)
    def __str__(self):
        return self.nombre_servicio

# Orden
class Orden(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    direccion = models.CharField(max_length=100, default='', blank=True)
    telefono = models.CharField(max_length=50, default='', blank=True)
    fecha = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.producto
    
    class Meta:
        verbose_name_plural = 'Ordenes'