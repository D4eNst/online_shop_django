from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from my_shop.forms import ProductForm

from my_shop.models import Product, Category, Size, Color, Sex, Designer, Brand, ProductSize, Photo


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    min_num = 1


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    min_num = 0


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'views_cnt', 'sex', 'category', 'is_active')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'descr')
    list_editable = ('is_active',)
    list_filter = ('sex', 'category', 'created_at', 'is_active',)
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('category', 'brand', 'designer',)
    inlines = [ProductSizeInline, PhotoInline]

    form = ProductForm


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Size)
class AdminSize(admin.ModelAdmin):
    pass


@admin.register(Color)
class AdminColor(admin.ModelAdmin):
    pass


@admin.register(Sex)
class AdminSex(admin.ModelAdmin):
    pass


@admin.register(Designer)
class AdminSex(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Brand)
class AdminSex(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Photo)
class AdminPhoto(admin.ModelAdmin):
    search_fields = ('photo',)


@admin.register(ProductSize)
class AdminProductSize(admin.ModelAdmin):
    pass