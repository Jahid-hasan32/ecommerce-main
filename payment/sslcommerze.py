from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse , HttpResponseRedirect
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Delivery_info, OrderItem 
from cart.models import Cart

def _cart_id(request):
    
    # If the user is anonymous, use their session key as the cart ID
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


# @login_required
def sslcommerz_payment_gateway(request):
    cartId = _cart_id(request)
    user = request.user
        
    order_item_instance   = OrderItem.objects.filter(cart_id = cartId)
    for get_prod_info in order_item_instance:                    
            get_user_add_instance = Delivery_info.objects.filter(cart_id = cartId) # getting the current user address
            for get_user_add in get_user_add_instance:  
                
                if request.method == "POST":
                    sslsettings = { 'store_id': settings.SSLCOMMERZ_STORE_ID, 'store_pass': settings.SSLCOMMERZ_STORE_PASSWORD, 'issandbox': True }
                    sslcz = SSLCOMMERZ(sslsettings)
                    post_body = {}
                    post_body['total_amount'] = get_prod_info.price
                    post_body['currency'] = "BDT"
                    post_body['tran_id'] = get_user_add.transaction_id
                    post_body['success_url'] = "http://127.0.0.1:8000/payment/success/"
                    post_body['fail_url'] = "http://127.0.0.1:8000/payment/fail/"
                    post_body['cancel_url'] = "http://127.0.0.1:8000/payment/cancel/"
                    post_body['emi_option'] = 0
                    post_body['cus_name'] = get_user_add.full_name
                    post_body['cus_email'] = get_user_add.email
                    post_body['cus_phone'] = get_user_add.phone_number
                    post_body['cus_add1'] = f' {get_user_add.district}, {get_user_add.address}'
                    post_body['cus_city'] = get_user_add.district
                    post_body['cus_country'] = "Bangladesh"
                    post_body['shipping_method'] = "NO"
                    post_body['multi_card_name'] = ""
                    post_body['num_of_item'] = get_prod_info.quanity
                    post_body['product_name'] = get_prod_info.products
                    post_body['product_category'] = get_prod_info.category
                    post_body['product_profile'] = "general"

                    response = sslcz.createSession(post_body) # API response
                    URL = response['GatewayPageURL']
                    return redirect(URL)
            return HttpResponse('Invalid Request')

@csrf_exempt
def succes(request):
    user = request.user
    if request.method == "POST":
        payment_data = request.POST
        status =  payment_data['status']
        if status == 'VALID':
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']
            amount = payment_data["currency_amount"]
            card_type = payment_data['card_type']
    
            url = reverse('payment:sslc_complete', args=(tran_id, val_id, amount, card_type))
            return HttpResponseRedirect(url)
        

# @login_required
def sslc_complete(request, tran_id, val_id, amount, card_type):
    user = request.user
    cartId = _cart_id(request)

    all_product_name = OrderItem.objects.filter(cart_id = cartId)    
    save_delivery_instance =  Delivery_info.objects.filter( cart_id = cartId)   
    
    for save_delivery in save_delivery_instance: 
        save_delivery.order_id = val_id
        save_delivery.paid = True
        save_delivery.status = 'Received'
        save_delivery.pay_system = card_type        
        save_delivery.orderd_products.add(*all_product_name)
        save_delivery.save()
    
    # all_product_name.delete()    
    
    # return redirect(request, 'payment/payment_success.html')
    return redirect('/')
    
def fail(request):
    return render(request, 'payment/payment_failed.html')

def cancel(request):
    return render(request, 'payment/payment_cancel.html')


def validate_IPN(request):
    
    sslsettings = { 'store_id': settings.SSLCOMMERZ_STORE_ID, 'store_pass': settings.SSLCOMMERZ_STORE_PASSWORD, 'issandbox': False }

    sslcz = SSLCOMMERZ(sslsettings)
    post_body = {}
    post_body['val_id'] = '200105225826116qFnATY9sHIwo'
    post_body['amount'] = "10.00"
    post_body['card_type'] = "VISA-Dutch Bangla"
    post_body['store_amount'] = "9.75"
    post_body['card_no'] = "418117XXXXXX6675"
    post_body['bank_tran_id'] = "200105225825DBgSoRGLvczhFjj"
    post_body['status'] = "VALID"
    post_body['tran_date'] = "2020-01-05 22:58:21"
    post_body['currency'] = "BDT"
    post_body['card_issuer'] = "TRUST BANK, LTD."
    post_body['card_brand'] = "VISA"
    post_body['card_issuer_country'] = "Bangladesh"
    post_body['card_issuer_country_code'] = "BD"
    post_body['store_id'] = "test_testemi"
    post_body['verify_sign'] = "d42fab70ae0bcbda5280e7baffef60b0"
    post_body['verify_key'] = "amount,bank_tran_id,base_fair,card_brand,card_issuer,card_issuer_country,card_issuer_country_code,card_no,card_type,currency,currency_amount,currency_rate,currency_type,risk_level,risk_title,status,store_amount,store_id,tran_date,tran_id,val_id,value_a,value_b,value_c,value_d"
    post_body['verify_sign_sha2'] = "02c0417ff467c109006382d56eedccecd68382e47245266e7b47abbb3d43976e"
    post_body['currency_type'] = "BDT"
    post_body['currency_amount'] = "10.00"
    post_body['currency_rate'] = "1.0000"
    post_body['base_fair'] = "0.00"
    post_body['value_a'] = ""
    post_body['value_b'] = ""
    post_body['value_c'] = ""
    post_body['value_d'] = ""
    post_body['risk_level'] = "0"
    post_body['risk_title'] = "Safe"
    if sslcz.hash_validate_ipn(post_body):
        response = sslcz.validationTransactionOrder(post_body['val_id'])
        print(response)
    else:
        print("Hash validation failed")
        