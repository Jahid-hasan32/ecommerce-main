from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap  # Import your sitemap class

sitemaps = {
    'products': ProductSitemap,  # Use a dictionary to map sitemap names to sitemap classes
}

urlpatterns = [
    path('',views.home, name="home"),
    path('sitemapxml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap_product_detail/<str:id>/', views.sitemap_product_detail, name ="sitemap_product_detail"),
    path('landing/<str:domain>/', views.landing_page, name='landing_page'),
    path('cart_section/', views.cart, name="cart"),
    path('produt-detail/<int:id>/ <str:name>/', views.prod_detail, name = "prod_detail"),
    path('prod_by_banner/<int:id>/<str:category>/', views.prod_by_banner, name= "prod_by_banner"),
    path('products_by/category/<str:id>/<slug:slug>/', views.product_by_cate, name='product_by_cate'),
    path('prod_by_subcate/<int:id>/<str:name>/', views.prod_by_subcate, name="prod_by_subcate"),
    path('featured-product/<str:name>/', views.featured_cate, name="featured_cate"),
    path('shop-by-brand/<str:name>/', views.shop_by_brand, name="shop_by_brand"),
    path('about-us/', views.about, name="about"),
    path('search/', views.search, name="search")
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
