from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Safazone Admin Panel"
admin.site.site_title = "Login to access Safazone admin"

urlpatterns = [
    # path('glass-fan/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('account/', include('account.urls')),
    path('cart/', include('cart.urls')),
    path('payment/', include('payment.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
