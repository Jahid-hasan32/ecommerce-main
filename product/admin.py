from django.contrib import admin

from .models import (
    ProductView,
    Featured_category,
    Brand,
    Product_images,
    Product
    )
# Register your models here.

@admin.register(Featured_category)
class AdminFeatured_category(admin.ModelAdmin):
    list_display = ['id','name','created_date']

class Product_imagesAdmin(admin.TabularInline):
    model = Product_images
    extra = 3

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'discounted_price','offer_percent','category','feature_product']
    search_fields = ('discounted_price','category','subcategory')
    inlines = [Product_imagesAdmin]


@admin.register(Brand)
class AdminBrand(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ProductView)
class AdminProductView(admin.ModelAdmin):
    list_display = ['id','user','product','timestamp']