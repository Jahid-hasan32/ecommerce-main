# from . models import Category

# def menu_links(request):
#     links =  Category.objects.values_list('slug', flat=True)
#     # links =  Category.objects.values('slug')
#     return dict(links = links)

from category.models import Category

def menu_links(request):
    categories = Category.objects.all()  # Retrieve all Category instances
    return {'categories': categories}



