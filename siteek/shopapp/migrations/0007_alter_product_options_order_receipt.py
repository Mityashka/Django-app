# Generated by Django 5.1.2 on 2024-11-19 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0006_order_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name', 'price']},
        ),
        migrations.AddField(
            model_name='order',
            name='receipt',
            field=models.FileField(null=True, upload_to='orders/receipts'),
        ),
    ]
