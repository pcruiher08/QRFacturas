from django.contrib import admin
from .models import Order
from django.utils.html import format_html

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'charge_amount', 'date_created', 'qr_code_image', 'invoice')

    def qr_code_image(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.qr_code.url))
        return "(No QR Code)"
    qr_code_image.short_description = 'QR Code'
