from django.core.management.base import BaseCommand
from my_shop.models import *
import random
import time
import string


sex_list = list(Sex.objects.all())
size_list = list(Size.objects.all())
color_list = list(Color.objects.all())
brand_list = list(Brand.objects.all())
designer_list = list(Designer.objects.all())
category_dict = {
    'm': list(Category.objects.filter(sex__short_name='m')),
    'w': list(Category.objects.filter(sex__short_name='w')),
    'k': list(Category.objects.filter(sex__short_name='k')),
}
image_path = {
    'm': 'previews/2023/06/07/man_with_the_belt.jpg',
    'w': 'previews/2023/06/07/girl_in_dark_suite.jpg',
    'k': 'temp/img_item_kid.jpg',
}


# Команда заполнения базы данных
class Command(BaseCommand):
    help = 'Fill the database with dummy data'

    def add_arguments(self, parser):
        parser.add_argument('num_records', type=int, help='Number of records to create')

    def handle(self, *args, **options):
        num_records = options['num_records']
        objects = []
        product_sizes = []
        for _ in range(num_records):
            title = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            slug = title + str(round(time.time(), 4))[-7:]
            descr = ' '.join([''.join(random.choices(string.ascii_lowercase, k=10)) for _ in range(5)])
            price = random.randint(5, 200) + 0.01*random.randint(0, 100)
            preview = image_path
            is_active = bool(random.randint(0, 2))
            sex = random.choice(sex_list)
            category = random.choice(category_dict[sex.short_name])
            brand = random.choice(brand_list)
            designer = random.choice(designer_list)

            obj = Product(title=title, slug=slug, descr=descr, price=price, preview=image_path[sex.short_name],
                          is_active=is_active, sex=sex, category=category, brand=brand, designer=designer)
            objects.append(obj)

            for size in random.sample(size_list, random.randint(1, 7)):
                for color in random.sample(color_list, random.randint(1, 3)):
                    product_sizes.append(ProductSize(
                        product=obj, size=size, color=color, quantity=random.randint(5, 20)
                    ))
        Product.objects.bulk_create(objects)
        ProductSize.objects.bulk_create(product_sizes)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_records} records.'))
