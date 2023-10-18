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

def _cart_id(request):
    
    # If the user is anonymous, use their session key as the cart ID
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


# @login_required
def order_save(request):
    user = request.user
    cartId = _cart_id(request)
    cart_instances = Cart.objects.filter(cart_id = cartId)
    
    # Iterate through each cart and create OrderItem instances
    for cart in cart_instances:
        product = cart.product  
        quantity = cart.quantity
        price = quantity * product.price
        category        =  cart.product.category.name

        # Create an OrderItem instance
        OrderItem.objects.create(
            products=cart,  # Assign the Cart instance, not the Product instance
            quanity=quantity,
            cart_id = cartId,
            price  = price,
            category = category,
            created_at=timezone.now()
        )

    # Redirect to the payment address form after creating OrderItem instances
    return redirect('/payment/payment-address')

# @login_required
def payment_address(request):
    user = request.user
    user_add_check = None
    cartId = _cart_id(request)

    cart_item = Cart.objects.filter(cart_id=cartId)

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
                price=total_price,
                quanity=product_count,
                cart_id=cartId,
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
        user_add_check = Delivery_info.objects.filter(cart_id=cartId).exists()
        print(user_add_check)
    except Exception as e :
        pass
        
    context = {
        'total_price' : total_price, 
        'form': form,
        'product_count' : product_count,
        'user_add_check' : user_add_check,
    }

    return render(request, 'payment/payment1.html', context)


