# Generated by Django 4.2.1 on 2023-06-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='sex',
        ),
        migrations.AddField(
            model_name='category',
            name='sex',
            field=models.ManyToManyField(db_index=True, to='my_shop.sex', verbose_name='Пол'),
        ),
    ]
