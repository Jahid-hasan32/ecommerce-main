from django.db import models
from product . models import Product


class Banner(models.Model):
    CHOICE_BANNER = (
        ('ADD', 'ADD'),
        ('SIDE', 'SIDE'),
        ('MAIN', 'MAIN'),
    )
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices=CHOICE_BANNER)
    image       = models.CharField(max_length=350)
    
    def __str__(self):
        return f"{self.category} -- {self.product.name}"
    
     