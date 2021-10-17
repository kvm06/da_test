from django.db.models import base
from django.shortcuts import render
from products.models import Categories, Category
from . import parser

# Create your views here.
def parse_products(request):
    """Парсит каталог из https://www.citilink.ru/catalog/noutbuki/ и отожает его на странице"""
    products = parser.parse()
    print(products)
    for product in products:
        get_cat, create_cat=Category.objects.get_or_create(name=product.get('category'), base_category=product.get('base_category'))
        get_base_cat, create_base_cat=Category.objects.get_or_create(name=product.get('base_category'))
        category=(get_cat or create_cat)
        base_category=(get_base_cat or create_base_cat)
        
        try:
            Categories.objects.get(category=category, base_category=base_category)
        except Categories.DoesNotExist:
            Categories.objects.create(category=category, base_category=base_category)

    return render(request, "products/products.html", {'products': products})
