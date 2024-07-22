# generador/urls.py

from django.urls import path
from .views import factura_view, success_view

urlpatterns = [
    path('factura/', factura_view, name='factura'),
    path('success/', success_view, name='success'),
]
