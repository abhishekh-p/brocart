from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from ordersapp.models import order,orderItem
from django.db import transaction
from productapp.models import product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random


from .models import customers


def register(request):
    """Register a new customer and linked auth User."""
    if request.method == "POST":
        # In your current form the "name" field is the username.
        username = (request.POST.get("name") or "").strip()
        password = (request.POST.get("password") or "").strip()

        # Optional extra fields – fine if they are empty for now.
        phone_number = (request.POST.get("phone_number") or "").strip()
        address = (request.POST.get("address") or "").strip()

        if not username or not password:
            return render(
                request,
                "register.html",
                {"error_message": "Username and password are required."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "register.html",
                {"error_message": "username already taken!!"},
            )

        if phone_number and customers.objects.filter(phone_number=phone_number).exists():
            return render(
                request,
                "register.html",
                {"error_message": "on this phone number already logined!!!"},
            )

        if not phone_number or not address:
            return render(
                request,
                "register.html",
                {"error_message": "Phone number and address are required."},
            )

        # try:
        #     with transaction.atomic():
        #         # Create auth user with username + password
        #         user = User.objects.create_user(username=username, password=password)

        #         # Create linked customer profile
        #         customers.objects.create(
        #             name=username,
        #             phone_number=phone_number,
        #             address=address,
        #             user=user,
        #         )
        # except Exception as e:
        #     # Show the real failure reason in the browser.
        #     return render(
        #         request,
        #         "register.html",
        #         {"error_message": f"Registration failed: {e}"},
        #     )


        # genarate 6 digit otp

        otp  = str(random.randint(100000,999999))

        # store registration information temberorly

        request.session["username"] = username

        request.session["password"] = password

        request.session["phone_number"] = phone_number

        request.session["address"] = address

        request.session["otp"] = otp

        # for now print in terminal

        print(otp)


        return redirect("verify_otp")

    return render(request, "register.html")




def log_in(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=user_name, password=password)
        admin_user=authenticate(request,username=user_name,password=password)

        

        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
            return redirect('admin_home')
        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            context = {'error_message': 'Invalid username or password.'}
            return render(request,'login.html',context)
    return render(request,'login.html') 

def log_out(request):
    logout(request)
    contex={'success_message':'you have been logged out successfully .'}
    return render(request,'login.html')

@login_required
def customer_profile(request):
    user_profile = customers.objects.get(user=request.user)

    cart_order = order.objects.filter(owner = user_profile,ORDER_STATUS = order.cart_stage,delete_status = order.LIVE)
    cart_item = orderItem.objects.filter(order__in = cart_order)

    context={"profile":user_profile,"cart_item":cart_item}
    return render(request,'customer_profile.html',context)


def product_detail(request, pk):
    """Show a single product by id."""
    prod = get_object_or_404(product, pk=pk, delete_status=product.LIVE)
    context = {'product': prod}
    return render(request, 'customer_profile.html', context)

def update_profile(request):
    customer = customers.objects.get(user = request.user)
    if request.method == "POST":
        customer.name = request.POST.get('name')
        customer.address = request.POST.get('address')

        customer.save()

        
        return redirect('customer_profile')
    
    context = {"customers":customer}
        
    return render(request,"update_profile.html",context)



def verify_otp(request):
    if request.method == "POST":

        enter_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')

        if enter_otp == saved_otp :
            username = request.session.get('username')
            password = request.session.get('password')
            phone_number = request.session.get('phone_number')
            address = request.session.get('address')

        #check again before creating user

            if User.objects.filter(username=username).exists():
                return render(request,"verify_otp.html",{"error_message":"username already exist!!!!"})

            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=username,password=password)
                    customers.objects.create(name = username,phone_number = phone_number,address =address, user = user)


                #clear temporary registration data

                request.session.pop('username',None)
                request.session.pop('password',None)
                request.session.pop('phone',None)
                request.session.pop('address',None)

                return redirect("login")
            
            except Exception as e:
                return render(request,'verify_otp.html',{"error_message":str(e)})

        else:
            return render(request,"verify_otp.html",{"error_message":"invalid OTP"})

    return render(request,"verify_otp.html")
        
        

        


       
            
                                   