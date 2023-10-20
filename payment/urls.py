from django.urls import path
from . import views

from . sslcommerze import sslcommerz_payment_gateway, succes, sslc_complete,  cancel,fail

app_name = 'payment'

urlpatterns = [
    path('payment-address/', views.payment_address, name="payment"),
    path('order_save/', views.order_save, name="order_save"),
    path('make-payment', views.payment, name="make_payment"),
    path('feed_payment/<str:name>/', views.feed_payment, name="feed_payment"),
    
    path('sslcommerz_payment_gateway/', sslcommerz_payment_gateway, name='sslcommerz_payment_gateway'),
    path('ssl_complete/<str:tran_id>/<str:val_id>/<str:amount>/<str:card_type>/', sslc_complete, name='sslc_complete'),
    path('cancel/', cancel, name="cancel"),
    path('success/', succes, name="succes"),
    path('fail/', fail, name="fail"),
]

