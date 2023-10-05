
#views.py   
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login
#from django.contrib.auth.models import User
from .models import CustomUser

# Create your views here.

def index(request):
    return render(request,'index.html')
def dashboard(request):
    return render(request,'dashboard.html')

def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']  # Make sure this matches your form field name
        user_type = request.POST['user_type']

        if password != confirm_password:
            # Handle password mismatch error
            return render(request, 'registration.html', {'error_message': 'Passwords do not match'})

        # Create a new user object
        user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
        # You may want to do additional processing here if needed

        return redirect('login')  # Redirect to login page after successful registration

    return render(request,'registration.html')
  

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect

def login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('username')
        password = request.POST.get('password')

        if loginusername and password:  # Use 'loginusername' here
            user = authenticate(request, username=loginusername, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = 'Username and password are required'
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')




    #def logout (request):
    #auth.logout(request)
    #return redirect('/')


 #<li>
                                    #{% if user.is_authenticated %}
                                     #   <a href="logout" class="btn btn-primary ml-lg-3">Logout</a>
                                    #{% else %}
                                     #   <a href="login" class="btn btn-primary ml-lg-3">Login/Signup</a>
                                    #{% endif %}
                                #</li>