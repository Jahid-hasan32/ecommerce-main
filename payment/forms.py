from .models import Delivery_info
from django import forms

from django import forms

class CustomerAddressForm(forms.Form):
    CHOICE_DIVISION = (
        ('Dhaka', 'Dhaka'),
        ('Barishal', 'Barishal'),
        ('Chattogram', 'Chattogram'),
        ('Khulna', 'Khulna'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Mymensingh', 'Mymensingh'),
        ('Sylhet', 'Sylhet'),
    )
    
    CHOICE_DISTRICT = (
        ('Dhaka', 'Dhaka'),
        ('Barishal', 'Barishal'),
        ('Chattogram', 'Chattogram'),
        ('Khulna', 'Khulna'),
        ('Rajshahi', 'Rajshahi'),
        ('Rangpur', 'Rangpur'),
        ('Mymensingh', 'Mymensingh'),
        ('Sylhet', 'Sylhet'),
        ('Laxmipur', 'Laxmipur'),
        ('Chandpur', 'Chandpur'),
        ('Kumillah', 'Kumillah'),
        ('Narayengonj', 'Narayengonj'),
        ('Noakhali', 'Noakhali'),
        ('Feni', 'Feni'),
    )

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            "placeholder": "Your full name"
        })
    )
    email = forms.EmailField(
        required=False,  # To make the email field optional
        widget=forms.EmailInput(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            "placeholder": "Email (optional)"
        })
    )
    phone_number = forms.CharField(
        widget=forms.NumberInput(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            "placeholder": "Phone number"
        })
    )

    division = forms.ChoiceField(
        choices=CHOICE_DIVISION,  # Use the CHOICE_DIVISION tuple here
        widget=forms.Select(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        })
    )
    
    district = forms.ChoiceField(
        choices= CHOICE_DISTRICT,
        widget=forms.Select(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
        })
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
            "placeholder": "Upazila, Apartment, suite, etc."
        })
    )

# class CustomerAddressForm(forms.ModelForm):
#     class Meta:
#         model =  Delivery_info
#         fields = '__all__'
#         exclude = ['orderd_product','status','transaction_id']
        
#     widgets = {
#         "full_name" : forms.TextInput(attrs={"class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline", "placeholder": "Your full name"}),
#         "email": forms.EmailInput(attrs={"class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline", "placeholder": "Email (optional)"}),
#         "phone_number": forms.NumberInput(attrs={"class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline", "placeholder": "Phone number"}),
#         "division": forms.Select(attrs={"class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"}),
#         "district": forms.Select(attrs={"class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"}),
#         "upazila": forms.TextInput(attrs={"class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline", "placeholder": "Upazila"}),
#         "appartment": forms.TextInput(attrs={"class": "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline", "placeholder": "Apartment, suite, etc."}),
#     }
    
    
    