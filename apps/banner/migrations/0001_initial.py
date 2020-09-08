# Generated by Django 2.2.1 on 2020-09-08 15:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Название (Крупный шрифт)')),
                ('description', models.CharField(max_length=255, null=True, verbose_name='Описание (меклий шрифт)')),
                ('url', models.CharField(blank=True, max_length=255, null=True, verbose_name='Сслыка на страницу')),
                ('image', models.ImageField(null=True, upload_to='', verbose_name='Картинка баннера')),
                ('image_thmb', models.TextField(blank=True, editable=False, null=True)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Последнее изменение (сортировка)')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ['-created'],
            },
        ),
    ]
