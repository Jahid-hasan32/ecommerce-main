from django.contrib import admin
from . models import Delivery_info, OrderItem , Transaction

    
@admin.register(Delivery_info)
class AdminDelivery_info(admin.ModelAdmin):
    list_display = ['id','full_name','phone_number','division','district','transaction_id','paid']
    search_fields = ['full_name','phone_number','division','district']

@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ['user','quanity','price','created_at','products']

@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    list_display = ['id', 'user', 'cus_phone','total_amount','transection_id']


# from .services import get_pathao_access_token, create_pathao_shipment

# def mark_as_delivered(modeladmin, request, queryset):
#     access_token = get_pathao_access_token()  # Obtain the Pathao access token
#     for delivery in queryset:
#         shipment_data = {
#             "tracking_number": delivery.tracking_number,
#             "status": "Delivered",
#             # Add other required shipment data here
#         }
#         create_pathao_shipment(shipment_data, access_token)

#         # Update the status in the database
#         delivery.status = 'Delivered'
#         delivery.save()

# mark_as_delivered.short_description = "Mark selected deliveries as Delivered"

# class DeliveryAdmin(admin.ModelAdmin):
#     list_display = ('transaction_id', 'recipient_name', 'status')
#     actions = [mark_as_delivered]

# admin.site.register(Delivery, DeliveryAdmin)