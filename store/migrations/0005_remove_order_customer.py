# Generated by Django 4.1.7 on 2023-03-07 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
    ]
