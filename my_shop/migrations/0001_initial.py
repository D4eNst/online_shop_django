# Generated by Django 4.2.1 on 2023-06-02 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='Название')),
                ('slug', models.SlugField(max_length=30, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='Название')),
                ('color', models.CharField(max_length=7, verbose_name='Код цвета')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Designer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Дизайнер',
                'verbose_name_plural': 'Дизайнеры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фотография')),
            ],
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название')),
                ('short_name', models.CharField(db_index=True, max_length=1, verbose_name='Короткое название')),
            ],
            options={
                'verbose_name': 'Пол',
                'verbose_name_plural': 'Пол',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=10, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, verbose_name='Название')),
                ('slug', models.SlugField(max_length=150, unique=True, verbose_name='URL')),
                ('descr', models.TextField(max_length=1500, verbose_name='Описание')),
                ('price', models.FloatField(default=0, verbose_name='Цена')),
                ('quantity', models.IntegerField(default=0, verbose_name='Количество')),
                ('preview', models.ImageField(upload_to='previews/%Y/%m/%d', verbose_name='Превью')),
                ('is_active', models.BooleanField(db_index=True, default=False, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('views_cnt', models.IntegerField(default=0, editable=False, verbose_name='Просмотров')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_shop.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_shop.category', verbose_name='Категория')),
                ('color', models.ManyToManyField(db_index=True, to='my_shop.color', verbose_name='Цвет')),
                ('designer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_shop.designer', verbose_name='Дизайнер')),
                ('sex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_shop.sex', verbose_name='Пол')),
                ('size', models.ManyToManyField(db_index=True, to='my_shop.size', verbose_name='Размер')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-created_at', 'title'],
            },
        ),
        migrations.AddField(
            model_name='category',
            name='sex',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_shop.sex', verbose_name='Пол'),
        ),
    ]
