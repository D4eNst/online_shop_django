from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from .models import Product, Sex, Category


class MainView(View):
    def get(self, request):
        context = {'title': 'Main page'}
        return render(request, 'my_shop/index.html', context=context)


class ProductListView(ListView):
    model = Product
    template_name = 'my_shop/product_list.html'
    context_object_name = 'products'

    categories = Category.objects.all()
    sex = Category.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.categories.get(slug=self.kwargs.get('category')).name
        return context

    def get_queryset(self):
        return Product.objects.filter(category=self.categories.get(slug=self.kwargs.get('category')).pk,
                                      sex=self.sex.get(short_name=self.kwargs.get('sex')).pk,
                                      is_active=True)


def choose_sex(request):
    sexs = Sex.objects.all()
    print(sexs)
    context = {
        'sex_list': sexs,
    }
    return render(request, 'my_shop/choose_sex.html', context=context)


def product_redirect_view(request, sex):
    category = 'new-arrivals'
    return redirect('product-list', sex='m', category=category)
