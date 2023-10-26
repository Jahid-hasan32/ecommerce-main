from django.shortcuts import render , get_object_or_404
from . models import Product, Featured_category , Brand , ProductView
from category.models import Category, Subcategory
from django.contrib.sites.shortcuts import get_current_site
from banners. models import Banner
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# main view
def home(request):

    new_arrival = Product.objects.filter(feature_product="new arrival", availabe = True)
    deal_of_day = Product.objects.filter(feature_product="deal of the day", availabe = True)
    best_deal = Product.objects.filter(feature_product="best deal", availabe = True)
    best_sellers = Product.objects.filter(feature_product="best sellers", availabe = True)
    new_arrival_gadget = Product.objects.filter(feature_product="new arrival gadget", availabe = True)
    
    products_without_feature = Product.objects.filter(Q(feature_product="") | Q(feature_product__isnull=True), availabe=True)
    
    shop_by_brand = Brand.objects.all()
    
    # banner fatching. 
    main_banners  = Banner.objects.filter(category = 'MAIN')
    side_banners  = Banner.objects.filter(category = 'SIDE')
    add_banners  = Banner.objects.filter(category = 'ADD')
        
    featured_category = Featured_category.objects.all()
    
    context = {
        'products_without_feature' : products_without_feature, 
        "new_arrival": new_arrival,
        "deal_of_day": deal_of_day,
        'best_deal' : best_deal, 
        'best_sellers' : best_sellers, 
        'new_arrival_gadget' : new_arrival_gadget, 
        'featured_category' : featured_category,
        'main_banners' : main_banners,
        'side_banners' : side_banners,
        'add_banners' : add_banners, 
        'shop_by_brand'  : shop_by_brand
    }

    return render(request, 'index.html', context)

# cart 
def cart(request):
    return render(request, 'cart.html')

# all products show
def all_product(request):
    get_all_product = Product.objects.all()
    return render(request, 'allproduct.html', {'get_all_product':get_all_product})

# Products by category. 
def product_by_cate(request, id, slug):
    product_cate     = Product.objects.filter( category__id = id, category__slug = slug)
    sub_category    = Subcategory.objects.filter(main_category__id = id,  main_category__slug = slug)
    
    cate_name = None
    for i in product_cate:
        cate_name = i.category.slug
            
    context = {
        'product_cate' : product_cate,
        'cate_name': cate_name,
        'sub_category' : sub_category,
    }
       
    return render(request, 'products_by_cate.html', context)

#product detail 
def prod_detail(request, id, name):
    get_product = Product.objects.get(id=id, name=name)
    category_prod = get_product.category
    get_product_by_category =  Product.objects.filter(category = category_prod)
    
    context = {
        'get_product' : get_product,
        'get_product_by_category' : get_product_by_category
    }
    return render(request, 'prod_detail.html', context)


# sub_cate_products 

def prod_by_subcate(request, id, name):
    prod_by_subcate = Subcategory.objects.filter(id=id, name=name)
    for i in prod_by_subcate:
        subc_name = i.name
        get_all_product_by_subcate = Product.objects.filter(subcategory__name = subc_name)

    context = {
        'get_all_product_by_subcate' : get_all_product_by_subcate
    }
    
    return render(request, 'prod_by_subcate.html', context)

# featured_categery

def featured_cate(request, name):

    get_fea_prod = Product.objects.filter(featured_category__name = name)
    
   
    context = {
        'name'  : name,
        'get_fea_prod'  : get_fea_prod,
    }
    
    return render(request, 'featured_cate.html', context)


# terms_condition
def terms_condition(request):
    return render(request, 'terms_condition.html')

# shop_by_brand

def shop_by_brand(request, name):
    
    get_prod_by_brand = Product.objects.filter(brand__name = name)
    
    context = {
        'name' : name,
        'get_prod_by_brand' : get_prod_by_brand
    }
    return render(request, 'shop_by_brand.html', context)


# about page
def about(request):
    return render(request, 'about.html')

# search option
def search(request):
    # get_prod_from_model_by_keyword = Product.objects.filter(name = name)
    
    if request.method == "POST":
        get_prod_from_input_by_keyword = request.POST['search']
        get_prod_from_model_by_keyword = Product.objects.filter(Q(name__icontains = get_prod_from_input_by_keyword) | Q(Description__icontains = get_prod_from_input_by_keyword))
    context = {
        "get_prod_from_model_by_keyword" : get_prod_from_model_by_keyword, 
    }
    return render(request, 'search.html', context)

# landing page for each product. 
# @login_required
def landing_page(request, id):
    landing = get_object_or_404(ProductView, id=id)
    return render(request, 'landing_page.html', {'landing': landing})


# contact defination
def contact(request):
    return render(request, 'contact.html')


# sitemap_product_detail
# def sitemap_product_detail(request, id):
#     get  = Product.objects.get(id = id)
#     return render(request, 'sitemap_product_detail.html', {'get':get})


