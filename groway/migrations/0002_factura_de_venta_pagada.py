# Generated by Django 3.0.7 on 2020-06-18 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura_de_venta',
            name='pagada',
            field=models.BooleanField(default=False),
        ),
    ]
