from tienda.models import *

class Carro():
    def __init__(self, request):
        self.session = request.session

        self.request = request

        # Obtener la key de la sesión si es que existe.
        carro = self.session.get('session_key')

        # Si el usuerio es nuevo, no hay sesión & se crea una.
        if 'session_key' not in request.session:
            carro = self.session['session_key'] = {}

        # Asegurar que carro este disponible en cualquier pág.
        self.carro = carro

    def db_agregar(self, producto, cantidad):
        producto_id = str(producto)
        producto_qty = str(cantidad)

        if producto_id in self.carro:
            pass
        else:
            # self.carro[producto_id] = {'precio': str(producto.precio)}
            self.carro[producto_id] = int(producto_qty)
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Perfil.objects.filter(usuario__id = self.request.user.id)
            carrojson = str(self.carro)
            carrojson = carrojson.replace("\'", "\"")

            current_user.update(carrito_viejo = str(carrojson))

    def agregar(self, producto, cantidad):
        producto_id = str(producto.id)
        producto_qty = str(cantidad)

        if producto_id in self.carro:
            pass
        else:
            # self.carro[producto_id] = {'precio': str(producto.precio)}
            self.carro[producto_id] = int(producto_qty)
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Perfil.objects.filter(usuario__id = self.request.user.id)
            carrojson = str(self.carro)
            carrojson = carrojson.replace("\'", "\"")

            current_user.update(carrito_viejo = str(carrojson))

    def __len__(self):
        return len(self.carro)
    
    def get_producto(self):
        producto_ids = self.carro.keys()
        productos = Producto.objects.filter(id__in=producto_ids)

        return productos
    
    def get_cantidades(self):
        cantidades = self.carro
        return cantidades
    
    def actualizar(self, producto, cantidad):
        producto_id = str(producto)
        producto_qty = int(cantidad)

        nuestrocarro = self.carro
        nuestrocarro[producto_id] = producto_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Perfil.objects.filter(usuario__id = self.request.user.id)
            carrojson = str(self.carro)
            carrojson = carrojson.replace("\'", "\"")

            current_user.update(carrito_viejo = str(carrojson))

        test = self.carro
        return test
    
    def eliminar(self, producto):
        producto_id = str(producto)
        if producto_id in self.carro:
            del self.carro[producto_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Perfil.objects.filter(usuario__id = self.request.user.id)
            carrojson = str(self.carro)
            carrojson = carrojson.replace("\'", "\"")

            current_user.update(carrito_viejo = str(carrojson))

    def eliminar_general(request):
        for key in list(request.session.keys()):
            if key == "session_key":
                del request.session[key]

    def carro_total(self):
        producto_ids = self.carro.keys()
        productos = Producto.objects.filter(id__in=producto_ids)

        cantidad = self.carro

        total = 0
        for key, value in cantidad.items():
            key = int(key)
            for producto in productos:
                if producto.id == key:
                    if producto.is_oferta:
                        total = total + (producto.oferta_precio * value)
                    else:
                        total = total + (producto.precio_final * value)

        return total