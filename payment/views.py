from django.shortcuts import render, redirect
from .models import Delivery_info, OrderItem
from cart.models import Cart
from .forms import CustomerAddressForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
import requests
from django.views.decorators.csrf import csrf_exempt
from . sslcommerze import sslcommerz_payment_gateway

@login_required
def order_save(request):
    user = request.user
    cart_instances = Cart.objects.filter(user=user)
    
    # Iterate through each cart and create OrderItem instances
    for cart in cart_instances:
        product = cart.product  
        quantity = cart.quantity
        price = quantity * product.price
        category        =  cart.product.category.name

        # Create an OrderItem instance
        OrderItem.objects.create(
            user=user,
            products=cart,  # Assign the Cart instance, not the Product instance
            quanity=quantity,
            price  = price,
            category = category,
            created_at=timezone.now()
        )

    # Redirect to the payment address form after creating OrderItem instances
    return redirect('/payment/payment-address')

@login_required
def payment_address(request):
    user = request.user
    user_add_check = None
            
    cart_item = Cart.objects.filter(user=user)

    total_price = 0
    product_count = 0
    
    for cart in cart_item:
        product_count += cart.quantity
        total_price = cart.quantity * cart.product.price
    if request.method == 'POST':
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            # Create an instance of your model and populate it with form data
            delivery_info, created = Delivery_info.objects.get_or_create(
                user=user,
                price=total_price,
                quanity=product_count,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone_number=form.cleaned_data['phone_number'],
                division=form.cleaned_data['division'],
                district=form.cleaned_data['district'],
                address=form.cleaned_data['address'],
            )
    else:
        form = CustomerAddressForm()
        
    try:
        user_add_check = Delivery_info.objects.filter(user=user).exists()
    except Exception as e :
        pass
        
    context = {
        'total_price' : total_price, 
        'form': form,
        'product_count' : product_count,
        'user_add_check' : user_add_check,
    }

    return render(request, 'payment/payment1.html', context)


