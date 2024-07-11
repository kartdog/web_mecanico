from django.urls import path, include
from rest_framework import routers
from . import views
from .views import *
from carro.views import generar_pdf
from django.contrib.auth import views as auth_views

# Configuracion urls para API
router = routers.DefaultRouter()
router.register('empleados', EmpleadoViewSet)
router.register('servicios', ServicioViewSet)
router.register('productos', ProductoViewSet)

urlpatterns = [
    # Index
    path('', views.index, name = 'index'),
    path('nosotros/', views.nosotros, name = 'nosotros'),
    # Productos
    path('productos/', views.productos, name="productos"),
    path('productos/<int:pk>', views.producto_id, name = 'producto_id'),
    path('productos/add/', views.productosadd, name="productosadd"),
    path('productos/crud/update/<id>/', views.productosupdate, name="productosupdate"),
    path('productos/crud/delete/<id>/', views.productosdelete, name="productosdelete"),
    # Servicios
    path('servicios/', views.servicios, name="servicios"),
    path('servicios/add/', views.serviciosadd, name="serviciosadd"),
    path('servicios/crud/update/<id>/', views.serviciosupdate, name="serviciosupdate"),
    path('servicios/crud/delete/<id>/', views.serviciosdelete, name="serviciosdelete"),
    # Categorias
    path('categoria/<str:foo>', views.categoria, name = 'categoria'),
    # Login
    path('accounts/login/', views.login_user, name= 'accounts/login/'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    # AXES
    path('account_locked/', views.account_locked, name='account_locked'),
    # Registro
    path('register/', views.register_user, name = 'register'),
    # Usuario
    path('actualizar_usuario/', views.actualizar_usuario, name = 'actualizar_usuario'),
    path('actualizar_info/', views.actualizar_info, name = 'actualizar_info'),
    # Empleados
    path('empleados/', views.empleados, name="empleados"),
    path('empleados/add/', views.empleadosadd, name="empleadosadd"),
    path('empleados/crud/update/<int:id>/', views.empleadosupdate, name="empleadosupdate"),
    path('empleados/crud/delete/<int:id>/', views.empleadosdelete, name="empleadosdelete"),
    # API
    path('api/', include(router.urls)),
    path('empleadosapi/', empleadosapi, name="empleadosapi"),
    path('serviciosapi/', serviciosapi, name="serviciosapi"),
    path('productosapi/', productosapi, name="productosapi"),
    # Recuperar contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),  # Reset de contraseña
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # Confirmación de envío de reset
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  # Confirmación de reset
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Completado de reset    
]