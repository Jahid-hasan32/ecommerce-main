from django.shortcuts import render,redirect
from .models import Cart 
from product.models import Product
from django.contrib.auth import get_user
from django.db.models import Q
from django.http import HttpResponse , JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

  
def _cart_id(request):
    # If the user is anonymous, use their session key as the cart ID
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id

def add_to_cart(request, id, name):
    user = request.user if request.user.is_authenticated else None
    cart_id = _cart_id(request)
    print('-----------------------')
    print(cart_id)
    print('-----------------------')
    
    get_product = get_object_or_404(Product, id=id, name=name)
    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(
            product=get_product,
            user = user,
            session_id=cart_id  # Use the cart_id function to get the cart identifier
        )
    else:        
        cart_item, created = Cart.objects.get_or_create(
            product=get_product,
            session_id=cart_id  # Use the cart_id function to get the cart identifier
        )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart/show-cart')

def showCart(request):
    user = request.user if request.user.is_authenticated else None

    # Use the cart_id function to get the cart identifier
    cart_id = _cart_id(request)

    product_count = []
    if request.user.is_authenticated:
        fetch_product_from_cart = Cart.objects.filter(session_id=cart_id, user = user)
    else:
        fetch_product_from_cart = Cart.objects.filter(session_id=cart_id)
    

    if fetch_product_from_cart:
        for cart_item in fetch_product_from_cart:
            product_count.append(cart_item.quantity)

    total_quantity = sum(product_count)

    amount = 0
    delivery_charge = 100
    total_amount = 0
    prod_from_cart = [p for p in Cart.objects.filter(session_id=cart_id, user=user)]

    if prod_from_cart:
        for product in prod_from_cart:
            tempAmount = product.quantity * product.product.price
            amount += tempAmount

    total_amount = amount + delivery_charge

    context = {
        'fetch_product_from_cart': fetch_product_from_cart,
        'product_count': total_quantity,
        'amount': amount,
        'total_amount': total_amount,
        'delivery_charge' : delivery_charge,
    }
    return render(request, 'cart.html', context)


# plus cart 
def pluscart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET.get('prod_id')
        
        if user.is_authenticated:
            cart_product = get_object_or_404(Cart, product=prod_id, user=user, session_id=_cart_id(request))
        else:
            cart_product = get_object_or_404(Cart, product=prod_id, session_id=_cart_id(request))
        
        cart_product.quantity += 1
        cart_product.save()
        
        prod_from_cart = Cart.objects.filter(user=user, session_id=_cart_id(request)) if user.is_authenticated else Cart.objects.filter(session_id=_cart_id(request))
        
        amount = sum(product.quantity * product.product.price for product in prod_from_cart)
        
        delivery_charge = 100
        total_amount = amount + delivery_charge
    
        data = {
            'total_amount': total_amount, 
            'quantity': cart_product.quantity,
            'amount': amount,   
            'delivery_charge':  delivery_charge,
        }
        return JsonResponse(data)
       
# minus cart
def minuscart(request):
    if request.method == 'GET':
        user = request.user
        prod_id = request.GET.get('prod_id')
        
        if user.is_authenticated:
            cart_product = get_object_or_404(Cart, product=prod_id, user=user, session_id=_cart_id(request))
        else:
            cart_product = get_object_or_404(Cart, product=prod_id, session_id=_cart_id(request))
        
        cart_product.quantity += 1
        cart_product.save()
        
        prod_from_cart = Cart.objects.filter(user=user, session_id=_cart_id(request)) if user.is_authenticated else Cart.objects.filter(session_id=_cart_id(request))
        
        amount = sum(product.quantity * product.product.price for product in prod_from_cart)
        
        delivery_charge = 100
        total_amount = amount + delivery_charge
    
        data = {
            'total_amount': total_amount, 
            'quantity': cart_product.quantity,
            'amount': amount,   
            'delivery_charge':  delivery_charge,
        }
        return JsonResponse(data) 
    
# remove cart
def remove_cart(request):
    if request.method == 'GET':
        user = get_user(request)
        prod_id = request.GET['prod_id']
        
        
        if user.is_authenticated:
            cart_product_id = get_object_or_404(Cart, product=prod_id, user=user)
        else:
            cart_product_id = get_object_or_404(Cart, product=prod_id, session_id=_cart_id(request))
        
        cart_product_id.delete()
        
        prod_from_cart = Cart.objects.filter(user=user, session_id=_cart_id(request)) if user.is_authenticated else Cart.objects.filter(session_id=_cart_id(request))
        
        amount = sum(product.quantity * product.product.price for product in prod_from_cart)
        
        delivery_charge = 100
        total_amount = amount + delivery_charge
    
        data = {
            'total_amount' : total_amount, 
            'quantity' : cart_product_id.quantity,
            'amount' : amount,   
        }
        return JsonResponse(data)

