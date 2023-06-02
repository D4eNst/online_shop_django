from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL')
    descr = models.TextField(max_length=1500, verbose_name='Описание')
    price = models.FloatField(default=0, verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество')
    preview = models.ImageField(upload_to='previews/%Y/%m/%d', verbose_name='Превью')
    is_active = models.BooleanField(default=False, db_index=True, verbose_name='Активный')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views_cnt = models.IntegerField(default=0, editable=False, verbose_name='Просмотров')

    sex = models.ForeignKey(to='Sex', on_delete=models.CASCADE, verbose_name='Пол', db_index=True)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, verbose_name='Категория', db_index=True)
    brand = models.ForeignKey(to='Brand', on_delete=models.CASCADE, verbose_name='Бренд', db_index=True)
    designer = models.ForeignKey(to='Designer', on_delete=models.CASCADE, verbose_name='Дизайнер', db_index=True)

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at', 'title', ]


class Sex(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    short_name = models.CharField(max_length=1, verbose_name='Короткое название', db_index=True)

    def get_filtered_products(self):
        return self.product_set.defer('category__name')

    filtered_products = property(get_filtered_products)

    def __str__(self):
        return self.name + ' (' + self.short_name + ')'

    class Meta:
        verbose_name = 'Пол'
        verbose_name_plural = 'Пол'
        ordering = ['id', ]


class Category(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название', db_index=True)
    slug = models.SlugField(max_length=30, unique=False, db_index=True, verbose_name='URL')
    sex = models.ManyToManyField(to='Sex', verbose_name='Пол', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', ]


class Size(models.Model):
    name = models.CharField(max_length=10, verbose_name='Название', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Color(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название', db_index=True)
    color = models.CharField(max_length=7, verbose_name='Код цвета')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name', ]


class Photo(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фотография')

    def __str__(self):
        return self.photo


class Brand(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name', ]


class Designer(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дизайнер'
        verbose_name_plural = 'Дизайнеры'
        ordering = ['name', ]


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name='Количество штук')

    class Meta:
        verbose_name = 'Размер товара'
        verbose_name_plural = 'Размеры товара'
