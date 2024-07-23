from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
import qrcode
from io import BytesIO
from django.core.files import File
import random
from django.shortcuts import render


# Vista personalizada para mostrar la lista de pedidos con sus códigos QR
def order_list(request):
    try:
        orders = Order.objects.all()
        return render(request, 'orders/order_list.html', {'orders': orders})
    except Exception as e:
        # Log the error message
        print(f"Error: {e}")
        # Return a generic error response
        return render(request, 'orders/order_list.html', {'orders': orders})

# Vista basada en viewsets para manejar las operaciones CRUD
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        charge_amount = request.data.get('charge_amount', None)
        if charge_amount is None:
            charge_amount = random.uniform(10.0, 100.0)  # Genera un cargo aleatorio por defecto
        
        order = Order(charge_amount=charge_amount)
        order.save()

        # Generar el código QR que apunta a una URL con el GUID
        #qr_url = f'http://127.0.0.1:8080/order-details/{order.id}/'
        qr_url = f'http://76.244.37.87:20002/order-details/{order.id}/'

        qr = qrcode.make(qr_url)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        order.qr_code.save(f'{order.id}.png', File(buffer), save=False)
        order.save()

        # Guardar en el archivo JSON
        order.save_to_json()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_invoice(self, request, pk=None):
        order = self.get_object()
        if order.invoice:
            return Response({"error": "Invoice already exists for this order"}, status=status.HTTP_400_BAD_REQUEST)
        
        invoice = request.data.get('invoice', None)
        if not invoice:
            return Response({"error": "Invoice must be provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        order.invoice = invoice
        order.save()

        # Guardar en el archivo JSON
        order.save_to_json()

        return Response({"success": "Invoice added successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_order_details(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    data = {
        'charge_amount': order.charge_amount,
        'date_created': order.date_created
    }
    
    return Response(data, status=status.HTTP_200_OK)