from django.contrib import admin

from . models import Banner



@admin.register(Banner)
class AdminBanner(admin.ModelAdmin):
    list_display = ['id','product','category']

