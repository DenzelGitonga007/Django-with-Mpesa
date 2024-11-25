from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.
# Register
def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                
                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('accounts:login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")
        
    return render(request, 'accounts/register.html')


# Login
def login_view(request):
    """ Login view """
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect("medi_app:home")
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'accounts/login.html')