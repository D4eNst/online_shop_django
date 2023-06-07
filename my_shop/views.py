from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.views.generic import View, ListView
from .models import Product, Brand, Designer, ProductSize, Sex


class MainView(View):
    def get(self, request):
        popular_products = Product.objects.filter(is_active=True).order_by('views_cnt')
        if popular_products.count() > 6:
            popular_products = popular_products[:6]
        context = {
            'title': 'Main page',
            'popular_products': popular_products
        }
        return render(request, 'my_shop/index.html', context=context)


class ProductListView(ListView):
    paginate_by = 12
    model = Product
    template_name = 'my_shop/product_list.html'
    context_object_name = 'products'

    category_name = None
    sex_name = None
    sizes = []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.category_name
        if self.category_name != 'global-search':
            context['sex'] = Sex.objects.get(short_name=self.sex_name)
        context['brands'] = Brand.objects.all()
        context['designers'] = Designer.objects.all()
        context['sizes'] = self.sizes
        return context

    def get_queryset(self):
        ordering = '-views_cnt'
        self.category_name = self.kwargs.get('category')
        self.sex_name = self.kwargs.get('sex')
        if self.category_name in ['global-search', 'new-arrivals']:
            self.sizes = list(ProductSize.objects.all().values_list('size__name', flat=True).distinct())
        else:
            self.sizes = list(ProductSize.objects.filter(product__category__slug=self.category_name).
                              values_list('size__name', flat=True).distinct())

        # я как-то получаю фильтры и формурую из них словарь (значения по умолчанию должны быть False)
        # макет весьма плох, я не знаю, как получить данные из фильтра
        # можно было бы сделать кнопку "сохранить фильтр" которая передавала бы в get запросе выбранные пункты
        # чтобы работала моя фильтрация, достаточно как раз получить от клиента необходимые списки:
        size_list = self.request.GET.get('size_list').split(',') if self.request.GET.get('size_list') else []
        brand = self.request.GET.get('brand').split(',') if self.request.GET.get('brand') else []
        designer = self.request.GET.get('designer').split(',') if self.request.GET.get('designer') else []
        search = self.request.GET.get('search', default='').lower().strip()

        filters = {
            'brand': brand,
            'designer': designer,
        }
        queryset_filter = {
            'is_active': True,
            'productsize__size__name__in': size_list if size_list else self.sizes,
        }
        if search:
            queryset_filter['title__icontains'] = search
        else:
            if self.category_name == 'new-arrivals':
                ordering = '-created_at'
                queryset_filter['created_at__gte'] = timezone.now() - timedelta(days=30)
            else:
                queryset_filter['category__slug'] = self.category_name

            queryset_filter['sex__short_name'] = self.sex_name

            for f, value in filters.items():
                if value:
                    queryset_filter[f'{f}__name__in'] = value
        return Product.objects.filter(
            **queryset_filter
        ).annotate(total_quantity=Sum('productsize__quantity')).filter(total_quantity__gt=0).order_by(ordering)


def choose_sex(request):
    return render(request, 'my_shop/choose_sex.html')


def product_redirect_view(request, sex):
    category = 'new-arrivals'
    return redirect('product-list', sex=sex, category=category)

# from my_shop.models import *
# c = Category.objects.prefetch_related('sex').all()
# s = Sex.objects.all()
# from django.db import *
# connection.queries
# for sex in s:
#     print(sex.name)
#     for category in c:
#         if sex in category.sex.all():
#             print(category.name)
