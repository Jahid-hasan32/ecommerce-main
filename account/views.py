from django.shortcuts import render
from django.http import HttpResponse
from . forms import UserCreation_form
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from  django.contrib import messages
from payment.models import Delivery_info

# user profile 

def profile(request):
    user = request.user
    delivery_info_instance = Delivery_info.objects.filter(user=user)
    
    for i in delivery_info_instance:
        order_id = i.order_id
        trans_id = i.transaction_id
        name = i.full_name
        phone = i.phone_number
        email = i.email
        division = i.division
        district = i.district
        address = i.address
        price = i.price
        product = i.orderd_products
        

    context = {
        'order_id' : order_id,
        'trans_id' : trans_id,
        'name' : name,
        'phone' : phone,
        'email' : email,
        'division' : division,
        'district' : district,
        'address' : address, 
        'price' : price,
        'product' : product
    }
    return render(request, 'account/profile.html', context) 


# ------> user registration form. 

class UserRegiForm(View):
    
    def get(self, request):
        form = UserCreation_form()
        user_register = False
        if request.user.is_authenticated:
            user_register = True
        context = {
            'form':form, 
            'user_register' : user_register
        }
        return render(request, 'account/user_regi_form.html', context  )
    
    def post(self, request):
        form = UserCreation_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'congratulations! successfully registerd!')
        return render(request, 'account/user_regi_form.html', {'form':form})



