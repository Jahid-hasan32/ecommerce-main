from django.db import models
import uuid
from django.urls import reverse
# from product.models import Product


# base model. 
class BaseModel(models.Model):
    name                     = models.CharField(max_length=300, unique=True)
    slug                       = models.SlugField(unique=True)
    created_date        = models.DateField(auto_now_add=True)
    
    class Meta:
        abstract = True

# Category Model. 
class Category(BaseModel):
    id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse("product_by_cate", args=[self.id, str(self.slug)])
    
# Subcategory Model. 
class Subcategory(BaseModel):
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    # product      = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date     = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        
    def __str__(self):
        return self.name
