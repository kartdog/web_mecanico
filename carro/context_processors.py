from .carro import Carro

# Crear procesador de contexto para que carro funcione en todas las págs.
def carro(request):
    # Devolver la info de nuestro carro.
    return{'carro': Carro(request)}