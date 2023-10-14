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

from django.template.loader import render_to_string

def generate_landing_content(product):
    context = {'product': product}
    return render_to_string('sitemap_product_detail.html', context)

@admin.register(ProductView)
class AdminProductView(admin.ModelAdmin):
    list_display = ['id','product', 'domain','created_at']
    list_filter = ('product',)
    search_fields = ('product__name', 'domain')
    
    def generate_landing_page(self, request, queryset):
        for landing in queryset:
            # Generate landing page for each product and set the domain
            # You can use a library like BeautifulSoup or a template engine to create HTML content.
            landing.content = generate_landing_content(landing.product)
            landing.save()

    actions = [generate_landing_page]