# Generated by Django 4.2.1 on 2023-06-02 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_shop', '0004_remove_product_color_remove_product_size_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sex',
            options={'ordering': ['id'], 'verbose_name': 'Пол', 'verbose_name_plural': 'Пол'},
        ),
    ]