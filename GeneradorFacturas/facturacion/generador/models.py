from django.db import models

class Factura(models.Model):
    id_factura = models.CharField(max_length=50, unique=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    correo = models.EmailField()
    rfc = models.CharField(max_length=13)
    otros_datos = models.TextField(blank=True)
    pdf_path = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.id_factura
