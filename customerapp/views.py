from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


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

        try:
            with transaction.atomic():
                # Create auth user with username + password
                user = User.objects.create_user(username=username, password=password)

                # Create linked customer profile
                customers.objects.create(
                    name=username,
                    phone_number=phone_number,
                    address=address,
                    user=user,
                )
        except Exception as e:
            # Show the real failure reason in the browser.
            return render(
                request,
                "register.html",
                {"error_message": f"Registration failed: {e}"},
            )

        return redirect("login")

    return render(request, "register.html")


def log_in(request):
    if request.method == "POST":
        user_name = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=user_name, password=password)
        admin_user=authenticate(request,username=user_name,password=password)

        

        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
            return redirect('home')
        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            context = {'error_message': 'Invalid username or password.'}
            return render(request,'login.html',context)
    return render(request,'login.html') 

def log_out(request):
    logout(request)
    return redirect(login)

@login_required
def profile(request):
    user_profile = customers.objects.get(user=request.user)
    context={"profile":user_profile}
    return render(request,'profile.html',context)