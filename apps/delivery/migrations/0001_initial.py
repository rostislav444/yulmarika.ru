# Generated by Django 2.2.1 on 2020-09-08 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_key', models.CharField(max_length=255, verbose_name='Ключ API')),
            ],
            options={
                'verbose_name': 'Доставка',
                'verbose_name_plural': 'Доставка',
            },
        ),
        migrations.CreateModel(
            name='DeliveryCities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название города')),
                ('name_lower', models.CharField(editable=False, max_length=255)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='delivery.Delivery')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
    ]
