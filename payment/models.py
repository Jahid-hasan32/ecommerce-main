from django.db import models
from cart.models import Cart
from account.models import User
from product.models import Product
from django.utils import timezone
import uuid

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=100, null=True ,default='')
    products  = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quanity         = models.PositiveIntegerField()
    price           = models.FloatField(default=0)
    category = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(default=timezone.now)    
    
    def __str__(self):
        return str(self.products)
    
# -> user info. 

class Delivery_info(models.Model):
    STATUS = ('Pending', 'Received', 'On The Way', 'Deliverd')
    
    cart_id = models.CharField(max_length=100, null=True ,default='')
    order_id             = models.CharField(max_length=100, default='')
    user                   = models.ForeignKey(User, on_delete=models.CASCADE, default='', null=True, blank=True)
    full_name          = models.CharField(max_length=200)
    email                 = models.EmailField(max_length=300, null=True, blank=True)
    phone_number = models.CharField(max_length=30)
    division             = models.CharField(max_length=100)
    district             = models.CharField(max_length=100)
    address              = models.CharField(max_length=300)
    orderd_products = models.ManyToManyField(OrderItem)
    transaction_id   = models.UUIDField(default=uuid.uuid4, unique=True)
    quanity         = models.PositiveIntegerField(default=0)
    price           = models.FloatField(default=0)
    status          = models.CharField(max_length=20, default='pending', choices=list(zip(STATUS, STATUS)))
    paid        = models.BooleanField(default=False)
    pay_system = models.CharField(max_length=100, default='')
    created_at  = models.DateField(auto_now=True)

    def __str__(self):
        return self.order_id
    


