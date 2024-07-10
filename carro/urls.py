from django.urls import path
from . import views

urlpatterns = [
    path('', views.carro_detalle, name="carro_detalle"),
    path('guardar_historial_compra/', views.guardar_historial_compra, name='guardar_historial_compra'),
    path('historial_compras', views.historial_compras, name='historial_compras'),
    path('agregar/', views.carro_agregar, name="carro_agregar"),
    path('eliminar/', views.carro_eliminar, name="carro_eliminar"),
    path('eliminar_general/', views.carro_eliminar_general, name="carro_eliminar_general"),
    path('actualizar/', views.carro_actualizar, name="carro_actualizar"),
    path('generar_pdf/<int:compra_id>/', views.generar_pdf, name='generar_pdf'),
]
