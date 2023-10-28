from django.urls import path
from . import views


urlpatterns = [ 
    path('add-to-cart/<int:id>/<str:name>/', views.order_now, name="order_now"),
    path('add-to-cart-auto/', views.add_to_cart, name="add_to_cart"),
    path('show-cart/', views.showCart, name = "showCart"),
    path('pluscart/', views.pluscart, name = "pluscart"),
    path('minuscart/', views.minuscart, name = "minuscart"),
    path('remove/', views.remove_cart, name = "remove"),
    path('check', views.check, name="check")
]


