from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
from django.contrib.auth.models import User
from admin_confirm import AdminConfirmMixin

class EmpleadoAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre','tipo','imagen']

class ProductoAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre','precio_final','descripcion']

class ServicioAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre_servicio','descripcion_servicio','imagen_servicio']

class CategoriaAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre']

class ClienteAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['p_nombre', 's_nombre', 'telefono', 'email', 'password']

class PerfilAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['usuario', 'date_modified', 'telefono', 'direccion', 'direccion_dos', 'ciudad', 'comuna', 'zipcode', 'pais', 'carrito_viejo']

class OrdenAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['producto', 'cliente', 'cantidad', 'direccion', 'telefono', 'fecha', 'status']

class CompraAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['usuario', 'productos', 'total_pagado', 'fecha_compra']

class CompraProductoAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['compra', 'producto', 'cantidad', 'precio']

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Perfil, PerfilAdmin)

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Servicio, ServicioAdmin)
admin.site.register(Orden, OrdenAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(CompraProducto, CompraProductoAdmin)

admin.site.register(Empleado, EmpleadoAdmin)

class PerfilInline(admin.StackedInline):
    model = Perfil

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["usuario", "p_nombre", "s_nombre", "email"]
    inlines = [PerfilInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)