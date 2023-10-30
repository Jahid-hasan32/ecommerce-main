from django.shortcuts import render,redirect
from .models import Cart 
from product.models import Product
from django.contrib.auth import get_user
from django.db.models import Q
from django.http import HttpResponse , JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

  
def _cart_id(request):
    # Get the session key if it exists
    cart_id = request.session.session_key
    
    # If the session key is not set, create a new session
    if not cart_id:
        request.session.save()  # Create and save a new session
        cart_id = request.session.session_key
    
    return cart_id

# order now

def order_now(request, id, name):
    user = request.user if request.user.is_authenticated else None
    cart_id = _cart_id(request)

    
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

def check(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        prod_name = request.GET.get('prod_name')

        data = {
            'prod_id' : prod_id,
            'prod_name' : prod_name
        }
        return JsonResponse(data)

#  add to cart 
def add_to_cart(request):
    user = request.user if request.user.is_authenticated else None
    cart_id = _cart_id(request)

    id = None
    name = None
    
    if request.method == 'GET':
        id = request.GET.get('prod_id')
        name = request.GET.get('prod_name')
        
        
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
        
    prod_count = Cart.objects.filter(session_id = cart_id)
    
    prod_counting = 0
    for pr_co in prod_count:
        prod_counting += pr_co.quantity
        
    data = {
        'prod_counting' : prod_counting
    }
    return JsonResponse(data)


def showCart(request):
    user = request.user if request.user.is_authenticated else None

    # Use the cart_id function to get the cart identifier
    cart_id = _cart_id(request)

    product_count = 0
    show_chekout_btn = False

    if request.user.is_authenticated:
        fetch_product_from_cart = Cart.objects.filter(session_id=cart_id, user = user)
    else:
        fetch_product_from_cart = Cart.objects.filter(session_id=cart_id)
    

    if fetch_product_from_cart:
        for cart_item in fetch_product_from_cart:
            product_count += cart_item.quantity
            
    # print('-------------------')
    # print(product_count)
    # print('-------------------') 
    
    if product_count >= 1 : # to disabled or un-disabled chekcout btn in cart page. 
        show_chekout_btn = True
        
    amount = 0
    prod_from_cart = [p for p in Cart.objects.filter(session_id=cart_id, user=user)]

    if prod_from_cart:
        for product in prod_from_cart:
            tempAmount = product.quantity * product.product.price
            amount += tempAmount


    context = {
        'fetch_product_from_cart': fetch_product_from_cart,
        'product_count': product_count,
        'amount': amount,
        'total_amount': amount, 
        'show_chekout_btn': show_chekout_btn, 
        
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
        
        cart_product.quantity += 1 # product increasing for authenticuser and anonymous
        cart_product.save()
        
        # product price calculation
        prod_from_cart = Cart.objects.filter(user=user, session_id=_cart_id(request)) if user.is_authenticated else Cart.objects.filter(session_id=_cart_id(request))
        amount = sum(product.quantity * product.product.price for product in prod_from_cart)
        
        
        data = {
            'total_amount': amount, 
            'quantity': cart_product.quantity,
            'amount': amount,   
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
        
        cart_product.quantity -= 1 # product decrement for authenticuser and anonymous
        cart_product.save()
        
        # product price calculation
        prod_from_cart = Cart.objects.filter(user=user, session_id=_cart_id(request)) if user.is_authenticated else Cart.objects.filter(session_id=_cart_id(request))
        amount = sum(product.quantity * product.product.price for product in prod_from_cart)
        
        
    
        data = {
            'total_amount': amount, 
            'quantity': cart_product.quantity,
            'amount': amount,   
        }
        return JsonResponse(data) 
    
# remove cart
def remove_cart(request):
    if request.method == 'GET':
        user = get_user(request)
        prod_id = request.GET['prod_id']
        
        
        if user.is_authenticated:
            cart_product = get_object_or_404(Cart, product=prod_id, user=user, session_id=_cart_id(request))
        else:
            cart_product = get_object_or_404(Cart, product=prod_id, session_id=_cart_id(request))
        
        cart_product.delete()  # product decrement for authenticuser and anonymous
        
        # product price calculation
        prod_from_cart = Cart.objects.filter(user=user, session_id=_cart_id(request)) if user.is_authenticated else Cart.objects.filter(session_id=_cart_id(request))
        amount = sum(product.quantity * product.product.price for product in prod_from_cart)
        
        
        data = {
            'total_amount' : amount, 
            'quantity' : cart_product.quantity,
            'amount' : amount,   
        }
        return JsonResponse(data)

