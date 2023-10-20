from django.contrib import admin
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import format_html

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
    list_display = ['id','product', 'current_site_url','created_at']
    # list_filter = ('product',)
    # search_fields = ('product__name', 'domain')
    
    def current_site_url(self, obj):
        # Get the current site dynamically
        current_site = get_current_site(self.request)

        # Determine the scheme (HTTP or HTTPS) based on the request
        scheme = 'https' if self.request.is_secure() else 'http'

        # Construct the full site URL using the scheme and current site's domain
        # site_url = f'{scheme}://{current_site}/seconde/'
        site_url = f'{scheme}://{current_site.domain}/landing/{obj.id}'

        # Make the URL clickable with an anchor tag
        return format_html('<a href="{}" target="_blank">{}</a>', site_url, site_url)

    current_site_url.short_description = 'Site URL'
    

    def current_site_domain(self, obj):
        # Get the current site dynamically
        current_site = get_current_site(self.request)
        return current_site.domain

    current_site_domain.short_description = 'Site Domain'

    def get_list_display(self, request):
        self.request = request
        return super().get_list_display(request)
    
