from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *
from django.contrib.auth.models import User
from admin_confirm import AdminConfirmMixin

class EmpleadoAdmin(AdminConfirmMixin, ModelAdmin):
    confirm_change = True
    confirmation_fields = ['nombre','tipo','imagen']

admin.site.register(Cliente)
admin.site.register(Perfil)

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(Servicio)
admin.site.register(Orden)
admin.site.register(Compra)
admin.site.register(CompraProducto)

admin.site.register(Empleado, EmpleadoAdmin)

class PerfilInline(admin.StackedInline):
    model = Perfil

class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["usuario", "p_nombre", "s_nombre", "email"]
    inlines = [PerfilInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)