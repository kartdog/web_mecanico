from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import *
from .carro import *
from tienda.models import *
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from reportlab.lib.pagesizes import letter
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas

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

# Historial
@login_required
def historial_compras(request):
    compras = HistorialCompra.objects.filter(usuario=request.user).order_by('-fecha')
    contexto = {
        "compras": compras
    }
    return render(request, 'historial.html', contexto)

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

@login_required
def guardar_historial_compra(request):
    if request.method == 'POST':
        carro = Carro(request)  # Assuming Carro is your cart manager class
        carro_productos = carro.get_producto()
        cantidades = carro.get_cantidades()
        total = carro.carro_total()

        # Prepare a list of dictionaries for productos
        productos_list = []
        for producto, cantidad in zip(carro_productos, cantidades):
            productos_list.append({
                'nombre': producto.nombre,
                'precio': str(producto.precio_final),  # Convert Decimal to string
                'cantidad': cantidad,
            })

        # Convert total to string
        total_str = str(total)

        # Convert contexto to JSON string
        contexto = {
            "productos": productos_list,
            "total": total_str,
        }
        
        # Save the purchase history
        compra = HistorialCompra(
            usuario=request.user,
            productos=json.dumps(contexto),  # Serialize contexto to JSON
            total=total
        )
        compra.save()

        return JsonResponse({"message": "Compra guardada con éxito"})

    return JsonResponse({"error": "Método no permitido"}, status=405)


def generar_pdf(request, compra_id=None):
    if compra_id:
        # Obtener una compra específica si se proporciona un compra_id
        compra = get_object_or_404(HistorialCompra, pk=compra_id, usuario=request.user)
        productos_data = json.loads(compra.productos)
        
        # Configurar la respuesta del PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="boleta_compra_{compra_id}.pdf"'
        
        # Inicializar el canvas de ReportLab
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Dibujar el contenido del PDF
        c.drawString(100, 750, 'Boleta de Compra')
        c.drawString(100, 730, f'Fecha: {compra.fecha.strftime("%d/%m/%Y %H:%M:%S")}')
        c.drawString(100, 710, f'Usuario: {compra.usuario.username}')
        c.drawString(100, 690, f'Total: ${compra.total}')
        
        # Dibujar los productos de la compra
        y = 670
        for producto in productos_data["productos"]:
            nombre = producto["nombre"]
            cantidad = producto["cantidad"]
            precio = producto["precio"]
            y -= 20
            c.drawString(120, y, f'Producto: {nombre} - Cantidad: {cantidad} - Precio: ${precio}')
        
        # Guardar el PDF y cerrar el canvas
        c.showPage()
        c.save()
        
        # Obtener el contenido del buffer y escribirlo en la respuesta
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        
        return response
    
    else:
        # Si no se proporciona un compra_id, redireccionar o manejar el error según sea necesario
        return HttpResponse("Error: No se proporcionó un ID de compra válido")

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