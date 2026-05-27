
from django.shortcuts import render, redirect, get_object_or_404
from .models import order, orderItem,payment
from productapp.models import product
from django.contrib.auth.decorators import login_required
from customerapp.models import customers
import razorpay
from django.conf import settings


# Create your views here.
@login_required
def get_or_create_cart(request):
    # Ensure every logged-in auth user has a linked customer profile.
    customer, _ = customers.objects.get_or_create(
        user=request.user,
        defaults={
            "name": request.user.username or "customer",
            "phone_number": "0000000000",
            "address": "not provided",
        },
    )

    cart, created = order.objects.get_or_create(
        owner=customer,
        ORDER_STATUS=order.cart_stage,
        delete_status=order.LIVE,
    )
    return cart

@login_required
def add_to_cart(request, pk):
    cart = get_or_create_cart(request)
    prod = get_object_or_404(product, id=pk)

    item, created = orderItem.objects.get_or_create(order=cart, products=prod)
    
    if not created:
        item.quantity += 1
        item.save()

    return redirect("view_cart")

@login_required
def view_cart_page(request): 
    cart = get_or_create_cart(request)
    items = cart.order_item.all()

    total = 0

    for item in items:
        if item.products:
            total += item.products.prize * item.quantity
    

    context = {'cart': cart, 'items': items, 'total': total}
    
    return render(request, 'cart_page.html', context)


@login_required
def check_out(request):

    cart = get_or_create_cart(request)
    item = cart.order_item.all()

    total = 0

    for items in item:
        if items.products:
            total += items.quantity * items.products.prize

    amount = int(total * 100)

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    razorpay_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    razorpay_order_id = razorpay_order['id']

    if request.method == 'POST':

        payment_type = request.POST.get('payment')

        # CASH ON DELIVERY
        if payment_type == 'cod':

            payment.objects.create(
                payment_method=payment.payment_cod,
                payment_order=cart
            )

            cart.ORDER_STATUS = order.ORDER_CONFIRMED
            cart.save()

            return redirect("order_success")

        # ONLINE PAYMENT
        elif payment_type == 'online':

            context = {
                "cart": cart,
                "item": item,
                "total": total,
                "razorpay_order_id": razorpay_order_id,
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
            }

            return render(request, "payment.html", context)

    context = {
        "cart": cart,
        "item": item,
        "total": total
    }

    return render(request, "checkout_page.html", context)

def success_page(request):
    return render(request,'success.html')







