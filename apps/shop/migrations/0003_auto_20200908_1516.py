# Generated by Django 2.2.1 on 2020-09-08 15:16

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20200908_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='hex',
            field=colorfield.fields.ColorField(blank=True, default=None, max_length=18, null=True, unique=True, verbose_name='Код цвета'),
        ),
    ]
