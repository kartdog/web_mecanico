from django.db import models
from django.contrib.auth.models import User

class HistorialCompra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    productos = models.TextField()  # Puedes usar JSONField si estás usando PostgreSQL
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra de {self.usuario.username} el {self.fecha}"
    
    def get_productos(self):
        import json
        return json.loads(self.productos)['productos']