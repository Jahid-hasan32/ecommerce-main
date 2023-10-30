from django.contrib import admin
from . models import Delivery_info, OrderItem 
import csv
from django.http import HttpResponse


def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="delivery_info.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone', 'Division','district', 'transaction_id', 'paid' ])  # Add column headers

    for obj in queryset:
        writer.writerow([obj.full_name, obj.phone_number, obj.division, obj.district, obj.transaction_id, obj.paid ])  # Add fields to export

    return response

export_to_csv.short_description = "Export selected records to CSV"

    
@admin.register(Delivery_info)
class AdminDelivery_info(admin.ModelAdmin):
    actions = [export_to_csv]
    list_display = ['session_id','full_name','phone_number','division','district','transaction_id','paid']
    search_fields = ['session_id','phone_number','division','district']

@admin.register(OrderItem)
class AdminOrderItem(admin.ModelAdmin):
    list_display = ['session_id','quanity','price','created_at','products']
    search_fields = ['session_id']

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