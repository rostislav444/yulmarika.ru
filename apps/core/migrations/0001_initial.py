# Generated by Django 2.2.1 on 2020-09-08 15:06

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackUpDB',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, verbose_name='Имя файла')),
                ('path', models.CharField(blank=True, max_length=300, verbose_name='Адрес файла')),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Дата дампа базы')),
                ('url', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Сслыка')),
                ('loaded', models.BooleanField(default=False, verbose_name='Загружен в облако')),
                ('response', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
        ),
    ]
