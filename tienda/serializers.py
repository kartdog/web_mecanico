from rest_framework import serializers
from .models import *

# Se transforman datos python a json.
class EmpleadoSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Empleado
        fields = '__all__'

class ServicioSerializers(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = '__all__'

class ProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'