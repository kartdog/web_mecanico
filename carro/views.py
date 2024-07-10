from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .carro import *
from tienda.models import *
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Render
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

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

def carro_detalle(request):

    carro = Carro(request)
    carro_productos = carro.get_producto()
    cantidades = carro.get_cantidades()
    total = carro.carro_total()

    #  API
    indicador = Mindicador('dolar', '2024')
    indicador_data = indicador.InfoApi()

    # Serie
    serie = indicador_data.get('serie', [])
    primer_item = serie[0] if serie else None

    contexto = {
        "carro_productos": carro_productos,
        "cantidades": cantidades,
        "total": total,
        "primer_item": primer_item,
    }

    return render(request, "carro_detalle.html", contexto)

def generar_pdf(request):
    carro = Carro(request)
    carro_productos = carro.get_producto()
    cantidades = carro.get_cantidades()
    total = carro.carro_total()

    contexto = {
        "carro_productos": carro_productos,
        "cantidades": cantidades,
        "total": total,
    }

    pdf = render_to_pdf('carro_pdf.html', contexto)

    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'carro_compras.pdf'
        content = f'attachment; filename="{filename}"'
        response['Content-Disposition'] = content
        return response
    
    # Maneja el caso en que no se puede generar el PDF
    return HttpResponse("Error al generar el PDF", status=500)

def carro_agregar(request):
    carro = Carro(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('producto_id'))
        producto_qty = int(request.POST.get('producto_qty'))

        producto = get_object_or_404(Producto, id=producto_id)
        carro.agregar(producto=producto, cantidad=producto_qty)

        carro_cantidad = carro.__len__()

        # response = JsonResponse({'Producto: ': producto.nombre})
        response = JsonResponse({'qty': carro_cantidad})
        messages.success(request, ("Producto agregado al carrito!"))
        return response

def carro_eliminar(request):
    carro = Carro(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('producto_id'))

        carro.eliminar(producto = producto_id)

        response = JsonResponse({'product': producto_id})
        messages.success(request, ("El producto se ha eliminado del carrito!"))
        return response
    
def carro_eliminar_general(request):
    if request.POST:
        if request.user.is_authenticated:
            for key in list(request.session.keys()):
                if key == "session_key":
					# Delete the key
                    del request.session[key]

            current_user = Perfil.objects.filter(usuario__id=request.user.id)
            current_user.update(carrito_viejo="")
            
            messages.success(request, ("Gracias por tu compra!"))
            return HttpResponse("Todos los productos del carrito han sido eliminados y el carrito viejo ha sido reiniciado.")
    return HttpResponse("Error: Acceso no autorizado o método no permitido.")

def carro_actualizar(request):
    carro = Carro(request)
    if request.POST.get('action') == 'post':
        producto_id = int(request.POST.get('producto_id'))
        producto_qty = int(request.POST.get('producto_qty'))

        carro.actualizar(producto= producto_id, cantidad = producto_qty)

        response = JsonResponse({'qty': producto_qty})
        messages.success(request, ("El carrito se ha actualizado!"))
        return response