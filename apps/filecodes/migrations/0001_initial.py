# Generated by Django 2.2.1 on 2020-09-08 15:06

import apps.filecodes.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', apps.filecodes.models.FileField(blank=True, null=True, upload_to='file_codes', verbose_name='Логотип сайта')),
                ('favicon', apps.filecodes.models.FileField(blank=True, null=True, upload_to='file_codes', verbose_name='Fav icon')),
                ('css', apps.filecodes.models.FileField(blank=True, null=True, upload_to='file_codes', verbose_name='Файлы стилей')),
                ('showcase', models.PositiveIntegerField(default=12, verbose_name='Колличесвто товаров на витрине')),
                ('recomend', models.PositiveIntegerField(default=24, verbose_name='Колличесвто товаров в блоке рекомендуем')),
                ('phone', models.CharField(max_length=255)),
                ('copyright', models.CharField(max_length=255, verbose_name='Текст копирайта футера')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок (приветствие)')),
            ],
            options={
                'verbose_name': 'Коды и файлы',
                'verbose_name_plural': 'Коды и файлы',
            },
        ),
        migrations.CreateModel(
            name='SocialIcons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название блока (всплывающая подсказака)')),
                ('url', models.CharField(max_length=500, verbose_name='Ссылка на ресурс')),
                ('icon', apps.filecodes.models.FileField(upload_to='icons', verbose_name='Иконка блока')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='icons', to='filecodes.FileCodes')),
            ],
            options={
                'verbose_name': 'Данные соц. сетей в футере',
                'verbose_name_plural': 'Данные соц. сетей в футере',
            },
        ),
    ]
