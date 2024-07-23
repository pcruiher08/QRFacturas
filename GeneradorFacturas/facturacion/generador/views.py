from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseServerError
from .forms import FacturaForm
from .models import Factura
from django.views.decorators.csrf import csrf_exempt
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def factura_view(request):
    if request.method == 'GET':
        guid = request.GET.get('guid')
        if guid:
            try:
                #response = requests.get(f'http://127.0.0.1:8000/order-details/{guid}')
                response = requests.get(f'http://76.244.37.87:20001/order-details/{guid}')
                
                response.raise_for_status()  # Check if the request was successful
                data = response.json()

                logger.debug(f'Datos recibidos de la API: {data}')  # Debugging output

                cantidad = data.get('charge_amount')
                fecha_str = data.get('date_created')

                # Convert the date format if the model uses DateField
                try:
                    fecha = datetime.fromisoformat(fecha_str.replace('Z', '+00:00')).strftime('%Y-%m-%d')
                except ValueError:
                    fecha = fecha_str  # Use the original format if conversion fails

                form = FacturaForm(initial={'cantidad': cantidad, 'fecha': fecha})
                return render(request, 'generador/factura_form.html', {'form': form, 'guid': guid})
            except requests.RequestException as e:
                logger.error(f'Error de solicitud: {e}')
                return HttpResponseServerError(f'Error al obtener datos de la API: {e}')
            except ValueError as e:
                logger.error(f'Error de decodificación JSON: {e}')
                return HttpResponseServerError(f'Error al decodificar JSON: {e}')
    elif request.method == 'POST':
        guid = request.POST.get('guid')
        cantidad = request.POST.get('cantidad')
        fecha_str = request.POST.get('fecha')
        correo = request.POST.get('correo')
        rfc = request.POST.get('rfc')
        otros_datos = request.POST.get('otros_datos')

        # Convert the date format if the model uses DateField
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            fecha = fecha_str  # Use the original format if conversion fails

        # Handle unique constraint
        try:
            factura, created = Factura.objects.update_or_create(
                id_factura=guid,
                defaults={
                    'cantidad': cantidad,
                    'fecha': fecha,
                    'correo': correo,
                    'rfc': rfc,
                    'otros_datos': otros_datos
                }
            )

            # Create directory if it does not exist
            pdf_dir = 'media/facturas/'
            os.makedirs(pdf_dir, exist_ok=True)

            # Generate PDF
            pdf_path = os.path.join(pdf_dir, f'{guid}.pdf')
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.drawString(100, 750, f'Factura ID: {guid}')
            c.drawString(100, 730, f'Cantidad: {factura.cantidad}')
            c.drawString(100, 710, f'Fecha: {factura.fecha}')
            c.drawString(100, 690, f'Correo: {factura.correo}')
            c.drawString(100, 670, f'RFC: {factura.rfc}')
            c.drawString(100, 650, f'Otros Datos: {factura.otros_datos}')
            c.save()

            # Save JSON
            json_data = {
                "invoice": {
                    'id_factura': guid,
                    'pdf_path': pdf_path
                }
            }

            json_file_path = os.path.join(pdf_dir, f'{guid}.json')
            with open(json_file_path, 'w') as json_file:
                json.dump(json_data, json_file)

            # Send POST request
            try:
                post_response = requests.post(f'http://76.244.37.87:20001/orders/{guid}/add_invoice/', json=json_data)
                post_response.raise_for_status()  # Check if the request was successful
            except requests.RequestException as e:
                logger.error(f'Error al enviar datos a la API: {e}')
                return HttpResponseServerError(f'Error al enviar datos a la API: {e}')

            return redirect('success')

        except Exception as e:
            logger.error(f'Error al crear o actualizar la factura: {e}')
            return HttpResponseServerError(f'Error al crear o actualizar la factura: {e}')

    return render(request, 'generador/factura_form.html', {'form': FacturaForm()})

def success_view(request):
    return render(request, 'generador/success.html')
