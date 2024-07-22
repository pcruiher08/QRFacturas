from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, order_list, get_order_details

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('order-list/', order_list, name='order_list'),
    path('order-details/<uuid:pk>/', get_order_details, name='get_order_details'),
]
