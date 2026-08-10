from django.shortcuts import render, get_object_or_404,redirect
from .models import product
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    """Home page view."""
    products = product.objects.filter(delete_status = product.LIVE)
    context = {'products':products}
    return render(request, 'index.html',context)


@login_required
def list_product(request):
    ''"list all product"''
    products = product.objects.filter(delete_status = product.LIVE)
    context = {'products':products}
    return render(request,'HOMEGPT.HTML',context)

def product_detail(request, pk):
    """Show a single product by id."""
    prod = get_object_or_404(product, pk=pk, delete_status=product.LIVE)
    context = {'product': prod}
    return render(request, 'product_detail.html', context)

def search_list_product(request):

    query = request.GET.get('q')

    products = product.objects.filter(
        delete_status=product.LIVE
    )

    if query:

        products = products.filter(
            title__icontains=query
        )

    context = {
        'products': products
    }

    return render(request, 'HOMEGPT.html', context)

#admin dashbord..................



@login_required
def admin_home_page(request):
    
    products = product.objects.all()
    context = {'products':products}
    return render(request,'admin_home.html',context)


def add_prduct(request):
    if request.method == 'POST':
        title = request.POST.get('title_name')
        prise = request.POST.get('prise')
        discription =request.POST.get('discription')
        image = request.FILES.get('image')

        product.objects.create(title=title,prize=prise,discription=discription,img=image)

        return redirect("admin_home")
    return render(request,"add_product.html")



def search_list_product(request):

    query = request.GET.get('q')

    products = product.objects.filter(
        delete_status=product.LIVE
    )

    if query:

        products = products.filter(
            title__icontains=query
        )

    context = {
        'products': products
    }

    return render(request, 'HOMEGPT.html', context)


def delete_product(request,pk):
    products = get_object_or_404(product,pk=pk)
    products.delete_status = product.DELETE
    products.save()
    return redirect("admin_home")


def edit_product(request,pk):
    product = get_object_or_404(product, pk = pk)
    if request.method == 'POST':
        product.title = request.POST.get('newttitle')
        product.prise = request.POST.get('newprise')
        product.diescription = request.POST.get('newdiscription')
        if request.FILES.get('newimage'):
            product.img = request.FILES.get("newimage")
        
        product.save()
        return redirect("admin_home")
    return render(request,'edit_producct.html',{'product':product})


def admin_search_product(request):
    query = request.GET.get('q')

    products = product.objects.filter(delete_status = product.LIVE)

    if query :

        products = product.objects.filter(title__icontains = query)

    context = {'products':products}

    return render(request,'admin_home.html',context)




