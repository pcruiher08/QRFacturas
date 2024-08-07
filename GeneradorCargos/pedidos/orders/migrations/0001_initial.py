# Generated by Django 5.0.7 on 2024-07-22 16:35

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("charge_amount", models.FloatField()),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "qr_code",
                    models.ImageField(blank=True, null=True, upload_to="qr_codes"),
                ),
            ],
        ),
    ]
