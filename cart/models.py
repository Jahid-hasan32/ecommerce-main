from django.db import models
from product.models import Product
from account.models import User

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_id = models.CharField(max_length=150)
    
    def __str__(self):
        return str(self.product)
    

