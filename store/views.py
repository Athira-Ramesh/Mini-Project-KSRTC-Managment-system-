
#views.py   
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.contrib import auth
from .models import Terminal
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from .models import Bus
from .models import Route, Bus
from .models import Staff_Allocation


# Create your views here.
@never_cache
def index(request):
    return render(request,'index.html')
@never_cache
def dashboard(request):
       return redirect('dashboard')
    #return render(request,'dashboard.html')
@never_cache
def admindashboard(request):
    return redirect('admindashboard')

@never_cache
def dashboard1(request):
    return redirect('dashboard1')


@never_cache
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        request.session['logged_out'] = True
    return redirect('index')
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

@never_cache
def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        posts = request.POST.get('posts')
        terminal = request.POST.get('terminal')

        if all([username, full_name, email, password, posts, terminal]):
            User = get_user_model()
            myuser = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            # Set additional custom fields
            myuser.full_name = full_name
            myuser.posts = posts
            myuser.terminal = terminal
            myuser.save()

            return redirect('login')
        else:
            # Handle the case where some form fields are missing or empty
            # You can add error handling or return a response indicating the issue.
            return render(request, 'registration.html')
    
    return render(request, 'registration.html')




@never_cache
#from django.contrib.auth import authenticate, login as auth_login
#from django.shortcuts import render, redirect



def login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('username')
        password = request.POST.get('password')


        if loginusername == "office" and password == "office123":
            # For the superuser, redirect to admin_index.html with user list and count
            users = CustomUser.objects.exclude(is_superuser='1')  # Exclude superusers
            user_count = users.count()
            context = {
                "users": users,
                "user_count": user_count
            }
            return render(request, 'admindashboard.html', context)
        else:
            user = authenticate(request, username=loginusername, password=password)

            if user is not None:
                auth_login(request, user)
                request.session['username'] = user.username
                if user.posts == 'conductor':
                    return redirect('dashboard')
                elif user.posts == 'driver':
                    return redirect('dashboard')
                else:
                    return redirect('admindashboard')
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})
    else:
            error_message = 'Username and password are required'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

    response = render(request,"login/login.html")
    response['Cache-Control'] = 'no-store,must-revalidate'
    return response



@never_cache
@login_required(login_url='login')
def dashboard(request):
    return render(request,'dashboard.html')

#def logout(request):
 #   try:
  #      del request.session['username']
  #  except:
   #     return redirect('login')
    #return redirect('login')

#def logout(request):
 #   auth_logout(request)
  #  return redirect('index')







@never_cache
@login_required(login_url='login')
def admindashboard(request):
    if request.user.is_superuser:
        users = CustomUser.objects.exclude(is_superuser=True)
        return render(request, "admindashboard.html", {"users": users})
    return redirect("home")

@never_cache
@login_required(login_url='login')
def dashboard(request):
    if 'username' in request.session:
        response = render(request,"dashboard.html")
        response['Cache-Control'] = 'no-store,must-revalidate'
        return response
    else:
        return redirect('login')

@never_cache
def handlelogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@never_cache
def logout(request):
    auth.logout(request)
    return redirect("/")



def terminal_add(request):
    if request.method == 'POST':
        terminal_name = request.POST.get('terminal_name')
        username = request.POST.get('username')
        location = request.POST.get('location')
        password = request.POST.get('password')

        if terminal_name and location and password:
            terminal = Terminal(terminal_name=terminal_name, username=username, location=location, password=password)
            terminal.save()  # Save the terminal data to the database
            return redirect('admindashboard')

    return render(request, 'terminal_add.html')
@never_cache
def view_staffs(request):
    return render(request,'view_staffs.html')


def deactivate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
         # Send deactivation email
        subject = 'Account Deactivation'
        message = 'Your account has been deactivated by the admin.'
        from_email = 'annmariyashaju2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('deactivation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)

        messages.success(request, f"User '{user.username}' has been deactivated, and an email has been sent.")
    else:
        messages.warning(request, f"User '{user.username}' is already deactivated.")
    return redirect('admindashboard')

def activate_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_active:
        user.is_active = True
        user.save()
        subject = 'Account activated'
        message = 'Your account has been activated.'
        from_email = 'annmariyashaju2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('admindashboard')    



def bus(request):
    if request.method == 'POST':
        registration_number = request.POST.get('registration_number')
        bus_number = request.POST.get('bus_number')
        status = request.POST.get('status')
        terminal_id = request.POST.get('terminal_id')

        if registration_number and bus_number and status and terminal_id:
            # Check if a bus with the given registration number already exists
            if Bus.objects.filter(registration_number=registration_number).exists():
                # Handle the case where the registration number is not unique
                return render(request, 'bus_add.html', {'error_message': 'This registration number is already in use'})

            terminal = Terminal.objects.get(terminal_id=terminal_id)  # Get the associated terminal
            bus = Bus(registration_number=registration_number, bus_number=bus_number, status=status, terminal=terminal)
            bus.save()  # Save the bus data to the database
            return redirect('admindashboard')  # Redirect to the bus list view

    # Fetch a list of unregistered terminals to display in the select field
    unregistered_terminals = Terminal.objects.exclude(bus__isnull=False)
    
    return render(request, 'bus_add.html', {'terminals': unregistered_terminals})


def bus_view(request, terminal_id):
    # Get the terminal by its ID
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    
    # Get the buses allocated to this terminal
    allocated_buses = terminal.bus_set.all()  # Assuming you have related_name='bus_set' in the Bus model
    
    return render(request, 'terminal_detail.html', {'terminal': terminal, 'allocated_buses': allocated_buses})




def route(request):
    if request.method == 'POST':
        source = request.POST.get('source', '')
        source_time = request.POST.get('source_time', '')
        destination = request.POST.get('destination', '')
        destination_time = request.POST.get('destination_time', '')
        busid = request.POST.get('bus', '')  # Retrieve the selected bus ID from the form

        if busid:
            try:
                busid = int(busid)  # Ensure that busid is a valid integer
                bus = Bus.objects.get(bus_id=busid)  # Get the bus object based on the selected bus ID
                route = Route(source=source, source_time=source_time, destination=destination, destination_time=destination_time, bus=bus)
                route.save()
                return redirect('admindashboard')  # Redirect to a success page
            except (Bus.DoesNotExist, ValueError):
                # Handle the case where the selected bus does not exist or busid is not a valid integer
                return render(request, 'route.html', {'error_message': 'Selected bus does not exist or invalid bus ID'})

    # For GET requests or when there are form validation errors, render the form
    buses = Bus.objects.all()  # Retrieve all available buses
    return render(request, 'route.html', {'buses': buses})



def route_view(request):
    routes = Route.objects.all()  # Query your database for the route data
    return render(request, 'route_view.html', {'routes': routes})  



def myprofile(request):
    return render(request, 'myprofile.html', {'user': request.user})   


@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Get updated data from the form
        username = request.POST['username']
        email = request.POST['email']
        full_name = request.POST['full_name']

        # Update the user's profile with the new data
        user = request.user
        user.username = username
        user.email = email
        user.full_name = full_name

        user.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('myprofile')

    return render(request, 'edit_profile.html', {'user': request.user})       



def bus_view(request):
    buses = Bus.objects.all()
    return render(request, 'bus_view.html', {'buses': buses})    


def edit_bus(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)

    if request.method == "POST":
        # Get the updated data from the request
        registration_number = request.POST['registration_number']
        bus_number = request.POST['bus_number']
        status = request.POST['status']
        terminal_id = request.POST['terminal_id']

        # Update the bus attributes
        bus.registration_number = registration_number
        bus.bus_number = bus_number
        bus.status = status
        # Update the terminal, if needed
        # bus.terminal_id = terminal_id
        # Save the changes
        bus.save()

        return redirect('bus_view')  # Redirect to the bus view page or another page
    else:
        return render(request, 'edit_bus.html', {'bus': bus})

def delete_bus(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)

    if request.method == "POST":
        # If the request is a POST request, delete the bus
        bus.delete()
        return redirect('bus_view')  # Redirect to the bus view page or another page

    return render(request, 'delete_bus.html', {'bus': bus})


from django.shortcuts import render, redirect
from .models import CustomUser, Terminal, Staff_Allocation

def staff_term(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        terminal_id = request.POST.get('terminal')
        allocation_date = request.POST.get('allocation_date')

        if not staff_id or not terminal_id or not allocation_date:
            return render(request, 'admindashboard.html', {'error_message': 'Please fill in all the fields'})

        try:
            staff = CustomUser.objects.get(id=staff_id)
            terminal = Terminal.objects.get(terminal_id=terminal_id)
            
            allocation = Staff_Allocation(staff=staff, terminal=terminal, allocation_date=allocation_date)
            allocation.save()
            
            return redirect('admindashboard')
        except (CustomUser.DoesNotExist, Terminal.DoesNotExist, ValueError):
            return render(request, 'allocation.html', {'error_message': 'Invalid staff or terminal selection'})

    staff_members = CustomUser.objects.all()
    terminals = Terminal.objects.all()
    
    return render(request, 'staff_term.html', {'staff_members': staff_members, 'terminals': terminals})

def viewstaff(request):
    allocations = Staff_Allocation.objects.all()  # Retrieve all allocation records
    return render(request, 'staff_term.html', {'allocations': allocations})    


