from django.contrib import sitemaps
from django.urls import reverse
from .models import Product

class ProductSitemap(sitemaps.Sitemap):
    changefreq = "daily"  # How often the content changes (e.g., daily, weekly)
    priority = 0.9  # Priority of this URL relative to others

    def items(self):
        return Product.objects.all()  # Return all product objects

    def location(self, obj):
        return reverse("sitemap_product_detail", args=[str(obj.id)])  # Assuming you have a URL pattern named "product_detail" for viewing a product
