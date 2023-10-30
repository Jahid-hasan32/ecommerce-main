from django.shortcuts import render, redirect
from .models import Delivery_info, OrderItem
from cart.models import Cart
from .forms import CustomerAddressForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.views.decorators.csrf import csrf_exempt
from . sslcommerze import sslcommerz_payment_gateway

def _cart_id(request):
    # Get the session key if it exists
    cart_id = request.session.session_key
    
    # If the session key is not set, create a new session
    if not cart_id:
        request.session.save()  # Create and save a new session
        cart_id = request.session.session_key
    
    return cart_id

# @login_required
def order_save(request):
    user = request.user
    cartId = _cart_id(request)
    cart_instances = Cart.objects.filter(session_id = cartId)
    
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
            session_id = cartId,
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

    cart_item = Cart.objects.filter(session_id=cartId)

    subtotal = 0
    product_count = 0
    
    for cart in cart_item:
        product_count += cart.quantity
        subtotal += cart.quantity * cart.product.price
        
    if request.method == 'POST':
        print(request.POST['payment'])
        # Create an instance of your model and populate it with form data
        delivery_info = Delivery_info.objects.create(
            total_price=subtotal,
            quantity=product_count,
            session_id=cartId,
            
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            division=request.POST.get('division'),
            district=request.POST.get('district'),
            address=request.POST.get('address'),
            
            payment = request.POST.get('payment'),
            transaction_number = request.POST.get('transactionNumber'),
            transaction_id = request.POST.get('transactionId'),   
            devliv_charge = request.POST.get('shping'),   
        )
        
        return redirect('/payment/feed_payment')
        
                
    context = {
        'subtotal' : subtotal, 
        'product_count' : product_count,
    }

    return render(request, 'payment/billing-add.html', context)


# payment 
def payment(request):
    return render (request, 'payment/payment.html')

# fedback after complete payment
def feed_payment(request):
    get_user_delivery_info = Delivery_info.objects.filter(session_id = _cart_id(request))
    
    for get_user_deliv_info in get_user_delivery_info:
        
        if get_user_deliv_info.payment == "Cash On":
            deli_charge_paid = "Yes"
        else:
            deli_charge_paid = "No"
        context = {
            'total_product' : get_user_deliv_info.quantity,
            'total_product_price' : get_user_deliv_info.total_price,
            'division' : get_user_deliv_info.division,
            'district' : get_user_deliv_info.district,
            'address' : get_user_deliv_info.address,
            'devlivery_charge': get_user_deliv_info.devliv_charge,
            'deli_charge_paid' : deli_charge_paid,
            'payment_method' : get_user_deliv_info.payment,
            'status' : get_user_deliv_info.status,
            'order_id' : get_user_deliv_info.order_id,
            'transaction_number' : get_user_deliv_info.transaction_number,
            'transaction_id' : get_user_deliv_info.transaction_id,
        }
        
    # cart_id = _cart_id(request)
    # Delete items from the Cart and OrderItem models
    # OrderItem.objects.filter(session_id=cart_id).delete()
    # Cart.objects.filter(session_id=cart_id).delete()
    
            
    return render(request, 'payment/payment_fedback.html', context)
