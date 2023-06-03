from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from .models import Product, Brand, Designer, ProductSize, Sex


class MainView(View):
    def get(self, request):
        context = {'title': 'Main page'}
        return render(request, 'my_shop/index.html', context=context)


class ProductListView(ListView):
    model = Product
    template_name = 'my_shop/product_list.html'
    context_object_name = 'products'

    category_name = None
    sex_name = None
    sizes = []

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.category_name
        context['sex'] = Sex.objects.get(short_name=self.sex_name)
        context['brands'] = Brand.objects.all()
        context['designers'] = Designer.objects.all()
        context['sizes'] = self.sizes
        return context

    def get_queryset(self):
        self.category_name = self.kwargs.get('category')
        self.sex_name = self.kwargs.get('sex')
        if self.category_name == 'global-search':
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
        # print(size_list, designer, brand, search, sep='\n')

        filters = {
            'size_list': size_list,
            'brand': brand,
            'designer': designer,
        }

        queryset_filter = {
            'is_active': True,
            'productsize__size__name__in': filters['size_list'] if filters['size_list'] else self.sizes,
        }
        if search:
            print('yes')
            queryset_filter['title__icontains'] = search
        else:
            print('no')
            queryset_filter['category__slug'] = self.category_name
            queryset_filter['sex__short_name'] = self.sex_name

            for f, value in filters.items():
                if value:
                    queryset_filter[f'{f}__name__in'] = value

        print(queryset_filter)
        return Product.objects.filter(
            **queryset_filter
        ).annotate(total_quantity=Sum('productsize__quantity')).filter(total_quantity__gt=0)


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
