from django.db import models
import uuid
import json
from datetime import datetime

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    charge_amount = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    invoice = models.CharField(max_length=255, blank=True, null=True, unique=True)
    
    def save_to_json(self):
        data = {
            str(self.id): {
                'charge_amount': self.charge_amount,
                'date_created': self.date_created.isoformat(),
                'qr_code': self.qr_code.url if self.qr_code else None,
                'invoice': self.invoice
            }
        }
        try:
            with open('orders.json', 'r+') as file:
                try:
                    orders = json.load(file)
                except json.JSONDecodeError:
                    orders = {}
                orders.update(data)
                file.seek(0)
                json.dump(orders, file, indent=4)
        except FileNotFoundError:
            with open('orders.json', 'w') as file:
                json.dump(data, file, indent=4)
