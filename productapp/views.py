from django.shortcuts import render, get_object_or_404
from .models import product

# Create your views here.

def index(request):
    """Home page view."""
    products = product.objects.all()
    context = {'products':products}
    return render(request, 'index.html',context)

def list_product(request):
    ''"list all product"''
    products = product.objects.all()
    context = {'products':products}
    return render(request,'HOMEGPT.HTML',context)

def product_detail(request, pk):
    """Show a single product by id."""
    prod = get_object_or_404(product, pk=pk, delete_status=product.LIVE)
    context = {'product': prod}
    return render(request, 'product_detail.html', context)
