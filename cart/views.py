from django.shortcuts import render,redirect
from .models import Cart 
from product.models import Product
from django.contrib.auth import get_user
from django.db.models import Q
from django.http import HttpResponse , JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

# add to cart 
@login_required
def add_to_cart(request, id, name):
    user = get_user(request)
    
    get_product =  get_object_or_404(Product, id= id, name=name)
    cart_item, created = Cart.objects.get_or_create(
        product = get_product, 
        user = user
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('/cart/show-cart')

# show cart
@login_required
def  showCart(request):
    user = get_user(request)
    
    # fetching the products from cart model . 
    fetch_product_from_cart = Cart.objects.filter(user = user )
    product_count = fetch_product_from_cart.count()
    
    amount = 0
    delivary_charge = 100
    total_amount = 0
    prod_from_cart = [p for p in Cart.objects.all() if p.user == user]

    if prod_from_cart:
        for product in prod_from_cart:
            tempAmount = product.quantity * product.product.price
            amount += tempAmount
    
    total_amount = amount + delivary_charge
    
    
    context = {
        'fetch_product_from_cart' : fetch_product_from_cart,
        'product_count' : product_count,
        'amount' : amount,
        'total_amount' : total_amount,

    }
    return render(request, 'cart.html', context)
    

# plus cart 
@login_required
def pluscart(request):
    if request.method == 'GET':
        user = get_user(request)
        prod_id = request.GET['prod_id']
        cart_product_id = Cart.objects.get(Q(product= prod_id) & Q(user = user))
        cart_product_id.quantity += 1
        cart_product_id.save()
        
        amount = 0
        delivary_charge = 100
        total_amount = 0
        prod_from_cart = [p for p in Cart.objects.all() if p.user == user]

        if prod_from_cart:
            for product in prod_from_cart:
                tempAmount = product.quantity * product.product.price
                amount += tempAmount
        
        total_amount = amount + delivary_charge
    
        data = {
            'total_amount' : total_amount, 
            'quantity' : cart_product_id.quantity,
            'amount' : amount,   
        }
        return JsonResponse(data)
    
# minus cart
@login_required
def minuscart(request):
    if request.method == 'GET':
        user = get_user(request)
        prod_id = request.GET['prod_id']
        cart_product_id = Cart.objects.get(Q(product= prod_id) & Q(user = user))
        cart_product_id.quantity -= 1
        cart_product_id.save()
        
        amount = 0
        delivary_charge = 100
        total_amount = 0
        prod_from_cart = [p for p in Cart.objects.all() if p.user == user]

        if prod_from_cart:
            for product in prod_from_cart:
                tempAmount = product.quantity * product.product.price
                amount += tempAmount
        
        total_amount = amount + delivary_charge
    
        data = {
            'total_amount' : total_amount, 
            'quantity' : cart_product_id.quantity,
            'amount' : amount,   
        }
        return JsonResponse(data)
    
# remove cart
@login_required
def remove_cart(request):
    if request.method == 'GET':
        user = get_user(request)
        prod_id = request.GET['prod_id']
        cart_product_id = Cart.objects.get(Q(product= prod_id) & Q(user = user))
        cart_product_id.delete()
        
        amount = 0
        delivary_charge = 100
        total_amount = 0
        prod_from_cart = [p for p in Cart.objects.all() if p.user == user]

        if prod_from_cart:
            for product in prod_from_cart:
                tempAmount = product.quantity * product.product.price
                amount += tempAmount
        
        total_amount = amount + delivary_charge
    
        data = {
            'total_amount' : total_amount, 
            'quantity' : cart_product_id.quantity,
            'amount' : amount,   
        }
        return JsonResponse(data)

