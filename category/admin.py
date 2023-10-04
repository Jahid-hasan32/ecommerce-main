from django.contrib import admin
from .models import Category , Subcategory
# Register your models here.

@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_date']
    search_fields  = ('name',)
    prepopulated_fields = {'slug': ['name']}

@admin.register(Subcategory)
class AdminSubcategory(admin.ModelAdmin):
    list_display = ['id','main_category',  'name', 'created_date']
    prepopulated_fields = {'slug':['name']}
    search_fields = ('name',)
