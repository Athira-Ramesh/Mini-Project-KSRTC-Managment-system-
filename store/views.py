
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
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control


# Create your views here.
@never_cache
def index(request):
    return render(request,'index.html')

@never_cache
def admindashboard(request):
    return redirect('admindashboard')



@never_cache
def term_staff_view(request):
    return redirect('term_staff_view')    


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
        terminal_id = request.POST.get('terminal')  # Get terminal ID

        if all([username, full_name, email, password, posts, terminal_id]):
            User = get_user_model()
            terminal = Terminal.objects.get(pk=terminal_id)  # Retrieve terminal object using ID
            myuser = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                posts=posts,
                terminal=terminal,  # Assign terminal object to user
                is_approved=False
            )

            return redirect('login')
        else:
            # Handle the case where some form fields are missing or empty
            # You can add error handling or return a response indicating the issue.
            return render(request, 'registration.html')
    
    # Get all terminals to populate the select field in the form
    terminals = Terminal.objects.all()
    return render(request, 'registration.html', {'terminals': terminals})


from django.shortcuts import get_object_or_404

def approve_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_approved = True
    user.save()
    return redirect('admindashboard')

def reject_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('admindashboard')    





#from django.contrib.auth import authenticate, login as auth_login
#from django.shortcuts import render, redirect


@never_cache
def login(request):
    if 'username' in request.session:
        return redirect(dashboard)
    if request.method == 'POST':
        loginusername = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the login is for a user
        user = authenticate(request, username=loginusername, password=password)
        if user is not None:
            if user.is_approved:
                auth_login(request, user)
                request.session['username'] = user.username
                if user.posts == 'conductor' or user.posts == 'driver':
                    return redirect('dashboard')
                elif user.posts == 'admin':
                    return redirect('admindashboard')
            else:
                error_message = 'Your account is pending approval.'
                return render(request, 'login.html', {'error_message': error_message})

        # Check if the login is for a terminal
        try:
            terminal = Terminal.objects.get(username=loginusername, password=password)
            # Add additional logic if needed for terminal login
            if terminal:
                context = {
                    'terminal': terminal,
                }
                return render(request, 'dashboard1.html', context)
        except Terminal.DoesNotExist:
            pass

        # Check if the login is for a workshop
        try:
            workshop = Workshop.objects.get(user_name=loginusername, password=password)
            if workshop:
                # Redirect to workshop.html upon successful login
                return render(request, 'workshop.html', {'workshop': workshop})
        except Workshop.DoesNotExist:
            pass

        # Check if the login is for the admin
        if loginusername == "office" and password == "office123":
            # For the superuser, redirect to admin_index.html with user list and count
            users = CustomUser.objects.exclude(is_superuser=True)  # Exclude superusers
            user_count = users.count()
            context = {
                "users": users,
                "user_count": user_count
            }
            return render(request, 'admindashboard.html', context)

        error_message = 'Invalid username or password'
        return render(request, 'login.html', {'error_message': error_message})

    # For GET requests, render the login form
    return render(request, 'login.html')
    


@never_cache
@login_required(login_url='login')
def dashboard(request):
    if 'username' is request.session: 
        return render(request, "home.html")
    return redirect(login)    
@never_cache
@login_required(login_url='login')
def dashboard1(request):
    if 'username' is request.session:
        return render(request, "home.html")
    return redirect(login)    


def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect(login)    


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
        from_email = 'athiraramesh2024a@mca.ajce.in'  # Replace with your email
        recipient_list = [user.email]
        html_message = render_to_string('activation_mail.html', {'user': user})

        send_mail(subject, message, from_email, recipient_list, html_message=html_message)
    else:
        messages.warning(request, f"User '{user.username}' is already active.")
    return redirect('admindashboard')    



from django.shortcuts import render, redirect
from .models import Terminal, Bus

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

            terminal = Terminal.objects.get(pk=terminal_id)  # Get the associated terminal
            bus = Bus(registration_number=registration_number, bus_number=bus_number, status=status, terminal=terminal)
            bus.save()  # Save the bus data to the database
            return redirect('admindashboard')  # Redirect to the bus list view

    # Fetch a list of all terminals
    all_terminals = Terminal.objects.all()

    return render(request, 'bus_add.html', {'terminals': all_terminals})



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

def allocate_terminal_staff(request):
    allocations = Staff_Allocation.objects.all()  # Retrieve all allocation records
    return render(request, 'staff_term.html', {'allocations': allocations})  





@login_required(login_url='login')
def dashboard1(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the terminal of the logged-in user
        terminal = request.user.terminal

        # Retrieve allocated staff for the user's terminal
        allocated_staff = Staff_Allocation.objects.filter(terminal=terminal)

        # Retrieve buses for the user's terminal
        buses = Bus.objects.filter(terminal=terminal)

        routes = Route.objects.filter(bus__in=buses)

        context = {
            'terminal': terminal,
            'allocated_staff': allocated_staff,
            'buses': buses,
            'routes': routes,
        }

        return render(request, 'dashboard1.html', context)
    else:
        # Handle the case where the user is not authenticated (AnonymousUser)
        # You can redirect them to the login page or handle it as needed
        return redirect('login')



def bus_route_view(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    routes = Route.objects.filter(bus=bus)

    context = {
        'bus': bus,
        'routes': routes,
    }

    return render(request, 'bus_route_view.html', context)     






from django.shortcuts import render, redirect
from .models import Bus, Terminal, BusAllocation

def allocate_bus(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus')
        terminal_id = request.POST.get('terminal')

        if bus_id and terminal_id:
            try:
                bus = Bus.objects.get(pk=bus_id)
                terminal = Terminal.objects.get(pk=terminal_id)

                BusAllocation.objects.create(bus=bus, terminal=terminal)
                return redirect('admindashboard')  # Redirect to a success page
            except (Bus.DoesNotExist, Terminal.DoesNotExist) as e:
                print(f"Exception: {e}")
                error_message = 'Selected bus or terminal does not exist'
        else:
            error_message = 'Please select both bus and terminal'

    buses = Bus.objects.all()
    terminals = Terminal.objects.all()

    return render(request, 'allocate_bus.html', {'buses': buses, 'terminals': terminals})






# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment, Bus, Staff_Allocation, Terminal
from django.utils import timezone

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Terminal, Staff_Allocation, BusAllocation, Assignment

def assign_terminal(request, terminal_id=None):
    terminal = get_object_or_404(Terminal, pk=terminal_id)
    error_message = None

    if request.method == 'POST':
        staff_allocation_id = request.POST.get('staff_allocation')
        bus_allocation_id = request.POST.get('bus_allocation')

        if staff_allocation_id and bus_allocation_id:
            try:
                staff_allocation = Staff_Allocation.objects.get(pk=staff_allocation_id, terminal=terminal)
                bus_allocation = BusAllocation.objects.get(pk=bus_allocation_id, terminal=terminal)

                if staff_allocation.terminal == bus_allocation.terminal:
                    Assignment.objects.create(
                        bus_allocation=bus_allocation,
                        staff_allocation=staff_allocation,
                    )
                    return redirect('dashboard1')  # Redirect to a success page
                else:
                    error_message = 'Selected staff is not allocated to the same terminal as the bus'
            except (Staff_Allocation.DoesNotExist, BusAllocation.DoesNotExist) as e:
                print(f"Exception: {e}")
                error_message = 'Selected staff, bus, or staff allocation does not exist or is not allocated to the same terminal'
        else:
            error_message = 'Please select both staff and bus'

    allocated_staff = Staff_Allocation.objects.filter(terminal=terminal)
    allocated_buses = BusAllocation.objects.filter(terminal=terminal)

    return render(request, 'assign_terminal.html', {'allocated_staff': allocated_staff, 'allocated_buses': allocated_buses, 'terminal': terminal, 'error_message': error_message})



from django.shortcuts import render, get_object_or_404
from .models import Assignment, Bus, Route
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required(login_url='login')
def dashboard(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the logged-in user
        user = request.user

        # Retrieve allocated staff for the user's terminal
        assigned_buses = Assignment.objects.filter(staff_allocation__staff=request.user)

        context = {
            'user': user,
            'assigned_buses': assigned_buses,
        }

        return render(request, 'dashboard.html', context)
    else:
        # Handle the case where the user is not authenticated (AnonymousUser)
        # You can redirect them to the login page or handle it as needed
        return redirect('login')


def staffrouteview(request, bus_id):
    bus = get_object_or_404(Bus, pk=bus_id)
    routes = Route.objects.filter(bus=bus)

    context = {
        'bus': bus,
        'routes': routes,
    }

    return render(request, 'staffrouteview.html', context)




from django.shortcuts import render, redirect
from .models import DailyCollection, Staff_Allocation, Assignment
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Staff_Allocation, Assignment, DailyCollection

def daily_collection_sent(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)

    # Assuming you have a way to get the current user's allocated terminals.
    allocated_terminals = Staff_Allocation.objects.filter(staff__id=user_id)
    assigned_buses = Assignment.objects.filter(staff_allocation__staff__id=user_id)

    context = {
        'allocated_terminals': allocated_terminals,
        'assigned_buses': assigned_buses,
    }

    if request.method == 'POST':
        staff_allocation_id = request.POST.get('staff_allocation')
        assignment_id = request.POST.get('assignment')
        collection_date = request.POST.get('collection_date')
        amount_collected = request.POST.get('amount_collected')

        # Modify the following line based on your actual model field
        staff_allocation = get_object_or_404(Staff_Allocation, pk=staff_allocation_id, staff__id=user_id)

        # Check if assignment_id is not an empty string
        if assignment_id:
            bus_assignment = get_object_or_404(Assignment, id=assignment_id, staff_allocation__staff__user=user)
        else:
            # Set a default assignment or handle the None case based on your requirements
            # In this example, we are using the first assigned bus as the default
            bus_assignment = assigned_buses.first()

        daily_collection = DailyCollection(
            staff_allocation=staff_allocation,
            assignment=bus_assignment,
            collection_date=collection_date,
            collection_amount=amount_collected
        )
        daily_collection.save()

        # Redirect to a success page or another page after the data is posted.
        return redirect('dashboard')

    return render(request, 'daily_collection_sent.html', context)




from django.shortcuts import render
from .models import DailyCollection

def daily_collection_view(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)
    # Assuming you want to display all daily collections
    daily_collections = DailyCollection.objects.all()

    context = {
        'daily_collections': daily_collections,
    }

    return render(request, 'daily_collection_view.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Terminal
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import Terminal

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Terminal

# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Terminal

def change_password(request, terminal_id):
    terminal = get_object_or_404(Terminal, terminal_id=terminal_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            # Passwords don't match, return a JSON response with an error
            return JsonResponse({'success': False, 'error': 'Passwords do not match'})

        terminal.password = new_password
        terminal.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    return render(request, 'change_password.html', {'terminal': terminal})




# views.py
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Staff_Allocation, Assignment, Complaint  # Import Complaint model

def complaint(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)

    # Assuming you have a way to get the current user's allocated terminals.
    allocated_terminals = Staff_Allocation.objects.filter(staff__id=user_id)
    assigned_buses = Assignment.objects.filter(staff_allocation__staff__id=user_id)

    context = {
        'allocated_terminals': allocated_terminals,
        'assigned_buses': assigned_buses,
    }

    if request.method == 'POST':
        staff_allocation_id = request.POST.get('staff_allocation')
        assignment_id = request.POST.get('assignment')
        complaint_date = request.POST.get('complaint_date')
        complaint_description = request.POST.get('collection_description')  # Corrected field name

        # Modify the following line based on your actual model field
        staff_allocation = get_object_or_404(Staff_Allocation, pk=staff_allocation_id, staff__id=user_id)

        # Check if assignment_id is not an empty string
        if assignment_id:
            bus_assignment = get_object_or_404(Assignment, id=assignment_id)
        else:
            # Set a default assignment or handle the None case based on your requirements
            # In this example, we are using the first assigned bus as the default
            bus_assignment = assigned_buses.first()

        complaint = Complaint(
            staff_allocation=staff_allocation,
            assignment=bus_assignment,
            complaint_date=complaint_date,
            complaint_description=complaint_description,  # Corrected field name
        )
        complaint.save()

        # Redirect to a success page or another page after the data is posted.
        return redirect('dashboard')

    return render(request, 'complaint.html', context)





from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Complaint

def user_complaints(request, user_id):
    user = get_object_or_404(get_user_model(), pk=user_id)

    # Fetch complaints associated with the user
    user_complaints = Complaint.objects.filter(staff_allocation__staff=user)

    context = {
        'user_complaints': user_complaints,
        'user': user,
    }

    return render(request, 'user_complaints.html', context) 




    from django.shortcuts import render, get_object_or_404, redirect
from .models import Route
from django.http import HttpResponse

def edit_route(request, route_id):
    route = get_object_or_404(Route, pk=route_id)

    if request.method == 'POST':
        # Update route details based on form data
        route.source = request.POST.get('source')
        route.source_time = request.POST.get('source_time')
        route.destination = request.POST.get('destination')
        route.destination_time = request.POST.get('destination_time')
        # Update other fields as needed
        route.save()
        return redirect('route_view')  # Redirect to the route list page

    # Debugging information
    print(f"Route ID: {route_id}")
    print(f"Route Object: {route}")

    return render(request, 'edit_route.html', {'route': route})

def delete_route(request, route_id):
    route = get_object_or_404(Route, route_id=route_id)

    if request.method == 'POST':
        # Delete the route
        route.delete()
        return redirect('route_view')  # Redirect to the route list page

    return render(request, 'delete_route.html', {'route': route})





from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Staff_Allocation, Assignment, Complaint

from django.shortcuts import render
from .models import Complaint

def view_complaint(request):
    # Retrieve all complaints
    complaints = Complaint.objects.all()

    context = {
        'complaints': complaints,
        # Add other context variables as needed
    }

    return render(request, 'admindashboard.html', context)




def view_terminal_complaints(request, terminal_id):
    terminal = get_object_or_404(Terminal, pk=terminal_id)

    # Filter complaints based on the terminal
    terminal_complaints = Complaint.objects.filter(staff_allocation__terminal=terminal)

    context = {
        'terminal': terminal,
        'terminal_complaints': terminal_complaints,
    }

    return render(request, 'view_terminal_complaints.html', context)



from django.shortcuts import render, get_object_or_404
from .models import DailyCollection, Staff_Allocation

from django.shortcuts import render, get_object_or_404
from .models import DailyCollection, Terminal  # Import your models

def view_term_daily_collection(request, terminal_id):
    # Retrieve the terminal or return a 404 response if it doesn't exist
    terminal = get_object_or_404(Terminal, pk=terminal_id)

    # Retrieve daily collections for the terminal
    terminal_daily_collections = DailyCollection.objects.filter(
        staff_allocation__terminal=terminal
    )

    context = {
        'terminal': terminal,  # Include the 'terminal' variable in the context
        'terminal_daily_collections': terminal_daily_collections,
    }

    return render(request, 'view_term_daily_collection.html', context)




from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .models import Complaint, ComplaintReply

def complaint_replay(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)
    terminal_id = None  # Initialize terminal_id
    
    if request.method == "POST":
        complaint_id = request.POST.get('complaint')
        reply_description = request.POST.get('reply_description')

        if complaint_id:  # Check if reply description is provided
            try:
                complaint = Complaint.objects.get(pk=complaint_id)
                new_reply = ComplaintReply.objects.create(
                    complaint=complaint,
                    reply_description=reply_description
                )
                return redirect('complaint_replay', complaint_id=complaint_id)
            except Exception as e:
                # Handle exceptions, e.g., if there's an issue creating the reply
                pass
    
    # Initialize terminal_id if the request method is not POST
    if complaint.staff_allocation and complaint.staff_allocation.terminal:
        terminal_id = complaint.staff_allocation.terminal.terminal_id
        
    return render(request, 'complaint_replay.html', {'complaint': complaint, 'terminal_id': terminal_id})





from django.shortcuts import render, redirect
from .models import Workshop
from store.models import Terminal  # Import Terminal model

def workshopadd(request):
    if request.method == 'POST':
        # Retrieve data from the request
        user_name = request.POST.get('user_name')
        location = request.POST.get('location')
        terminal_id = request.POST.get('terminal')  # Assuming the value is the terminal ID
        password = request.POST.get('password')

        # Retrieve the Terminal object based on the terminal_id
        terminal = Terminal.objects.get(pk=terminal_id)

        # Create a new Workshop instance and assign the password
        workshop = Workshop(user_name=user_name, location=location, terminal=terminal, password=password)
        workshop.save()

        # Redirect to a success page or another view
        return redirect('admindashboard')  # Define your success URL

    # If it's a GET request or form submission failed, render the template
    terminals = Terminal.objects.all()  # Retrieve all terminals
    context = {'terminals': terminals}
    return render(request, 'workshopadd.html', context)





from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from .models import Workshop
from store.models import Terminal

def change_pass(request, workshop_id):
    workshop = get_object_or_404(Workshop, workshop_id=workshop_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            # Passwords don't match, return a JSON response with an error
            return JsonResponse({'success': False, 'error': 'Passwords do not match'})

        workshop.password = new_password
        workshop.save()

        # Return a JSON response indicating success
        return JsonResponse({'success': True})

    return render(request, 'change_pass.html', {'workshop': workshop})




from django.shortcuts import render
from .models import WorkshopComplaint, Workshop

def workshop_complaint(request, user_id):
    workshops = Workshop.objects.all()

    if request.method == 'POST':
        complaint_description = request.POST.get('complaint_description')
        staff_id = request.user.id
        workshop_id = request.POST.get('workshop')
        date = request.POST.get('date')
        phone_number = request.POST.get('phone_number')
        latitude = request.POST.get('latitude')  # Retrieve latitude from the form
        longitude = request.POST.get('longitude')  # Retrieve longitude from the form

        # Validate all required fields
        if not (complaint_description and staff_id and workshop_id and date and phone_number and latitude and longitude):
            return render(request, 'workshop_complaint.html', {'error_message': 'All fields are required!', 'workshops': workshops})

        # Convert workshop_id to an integer
        try:
            workshop_id = int(workshop_id)
        except ValueError:
            return render(request, 'workshop_complaint.html', {'error_message': 'Invalid workshop ID!', 'workshops': workshops})

        # Create the WorkshopComplaint instance
        try:
            workshop_complaint = WorkshopComplaint.objects.create(
                complaint_description=complaint_description,
                staff_id=staff_id,
                workshop_id=workshop_id,
                date=date,
                phone_number=phone_number,
                latitude=latitude,  # Assign latitude to the model field
                longitude=longitude  # Assign longitude to the model field
            )
            workshop = Workshop.objects.get(pk=workshop_id)
            Notification.objects.create(recipient=workshop.user, message='New complaint submitted')
            return render(request, 'dashboard.html', {'success_message': 'Workshop complaint submitted successfully!'})
        except Exception as e:
            return render(request, 'workshop_complaint.html', {'error_message': f'An error occurred: {str(e)}', 'workshops': workshops})

    return render(request, 'workshop_complaint.html', {'workshops': workshops})





from django.shortcuts import render
from .models import Workshop

def view_workshop(request):
    workshops = Workshop.objects.all()
    context = {'workshops': workshops}
    return render(request, 'view_workshop.html', context)






from django.shortcuts import render, redirect, get_object_or_404
from .models import Workshop, Terminal  # Import Workshop and Terminal models

def edit_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    
    if request.method == 'POST':
        # Retrieve data from the request
        user_name = request.POST.get('user_name')
        location = request.POST.get('location')
        terminal_name = request.POST.get('terminal')  # Assuming the value is the terminal name
        password = request.POST.get('password')

        # Retrieve the Terminal object based on the terminal_name
        terminal = get_object_or_404(Terminal, terminal_name=terminal_name)

        # Update the Workshop instance with the new data
        workshop.user_name = user_name
        workshop.location = location
        workshop.terminal = terminal
        workshop.password = password
        workshop.save()

        # Redirect to a success page or another view
        return redirect('view_workshop')  # Define your success URL

    # If it's a GET request or form submission fails, render the template
    terminals = Terminal.objects.all()  # Retrieve all terminals
    context = {'workshop': workshop, 'terminals': terminals}
    return render(request, 'edit_workshop.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Workshop

def delete_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    
    if request.method == 'POST':
        # Check if the workshop exists
        if workshop:
            # Delete the workshop
            workshop.delete()
            return redirect('view_workshop')  # Redirect to the workshop list page
        else:
            return redirect('view_workshop')  # Redirect to the workshop list page if workshop doesn't exist
    
    # If it's a GET request, render the confirmation page
    return render(request, 'delete_workshop.html', {'workshop': workshop})



from django.shortcuts import render

def chat(request):
    # Your chat view logic here
    return render(request, 'chat.html')    













from django.shortcuts import render
from .models import WorkshopComplaint

def view_complaints(request, user_id):
    # Query complaints posted by the user
    user_complaints = WorkshopComplaint.objects.filter(staff_id=user_id)
    
    return render(request, 'view_complaints.html', {'user_complaints': user_complaints})





from django.shortcuts import render, get_object_or_404, redirect
from .models import WorkshopComplaint

def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(WorkshopComplaint, pk=complaint_id)
    
    if request.method == 'POST':
        complaint_description = request.POST.get('complaint_description')
        phone_number = request.POST.get('phone_number')
        
        # Update complaint fields
        complaint.complaint_description = complaint_description
        complaint.phone_number = phone_number
        # Save the updated complaint
        complaint.save()
        
        # Redirect to view_complaints or any other appropriate view
        return redirect('view_complaints', user_id=request.user.id)
    
    return render(request, 'edit_complaint.html', {'complaint': complaint})




def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(WorkshopComplaint, pk=complaint_id)
    
    if request.method == 'POST':
        # Process the form submission for deleting the complaint
        complaint.delete()
        return redirect('view_complaints', user_id=request.user.id)
    
    return render(request, 'delete_complaint.html', {'complaint': complaint})



@never_cache
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))




from django.shortcuts import render
from django.http import JsonResponse

def chatbot(request):
    return render(request, 'chatbot.html')

from django.http import JsonResponse

def chatbot_response(request):
    message = request.GET.get('message', '').strip().lower()
    response = get_chatbot_reply(message)
    return JsonResponse({'reply': response})

def get_chatbot_reply(message):
    if message == 'hi' or message == 'hello':
        return "Hello! How can I help you?"
    elif message == 'how are you':
        return "I'm fine, thank you for asking!"
    elif message == 'what is your name' or message == 'your name':
        return "I'm ChatBot, nice to meet you! How can I assist you today?"    
    else:
        return "I'm not trained in this."



from django.shortcuts import render, get_object_or_404
from .models import WorkshopComplaint

def gview(request, complaint_id):
    complaint = get_object_or_404(WorkshopComplaint, pk=complaint_id)
    context = {
        'complaint_latitude': complaint.latitude,
        'complaint_longitude': complaint.longitude,
    }
    return render(request, 'gview.html', context)






from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ComplaintResponse, WorkshopComplaint

def view_workshop_complaint(request, workshop_id):
    workshop = Workshop.objects.get(pk=workshop_id)
        
    # Adjust the query based on your model relationships
    workshop_complaint = WorkshopComplaint.objects.filter(workshop_id=workshop_id)
    
    context = {
        'workshop': workshop,
        'workshop_complaint': workshop_complaint,
    }
    
    return render(request, 'view_workshop_complaint.html', context)

def work_com_res(request, complaint_id):
    workshop_complaint = WorkshopComplaint.objects.get(pk=complaint_id)

    if request.method == 'POST':
        response_description = request.POST.get('response_description')

        # Create the ComplaintResponse instance
        complaint_response = ComplaintResponse.objects.create(
            workshop_complaint=workshop_complaint,
            response_description=response_description
        )

        # Set response submitted status for WorkshopComplaint
        workshop_complaint.response_submitted = True
        workshop_complaint.save()

        return redirect('view_workshop_complaint', workshop_id=workshop_complaint.workshop_id)

    return render(request, 'work_com_res.html')






from django.shortcuts import render, get_object_or_404
from .models import WorkshopComplaint, ComplaintResponse

def view_com_res(request, complaint_id):
    complaint = get_object_or_404(WorkshopComplaint, pk=complaint_id)
    response = complaint.complaintresponse_set.first()  # Assuming only one response per complaint
    context = {'complaint': complaint, 'response': response}
    return render(request, 'view_com_res.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from .models import ComplaintResponse

def edit_response(request, response_id):
    response = get_object_or_404(ComplaintResponse, pk=response_id)
    
    if request.method == 'POST':
        new_description = request.POST.get('response_description')
        response.response_description = new_description
        response.save()
        return redirect('view_com_res', complaint_id=response.workshop_complaint_id)
    
    context = {'response': response}
    return render(request, 'edit_response.html', context)



def get_new_complaints(request):
    # Logic to retrieve new complaints from the database
    new_complaints = WorkshopComplaint.objects.filter(is_new=True)  # Assuming you have a field to track new complaints

    # Return new complaints data as JSON
    data = [{'id': complaint.id, 'description': complaint.complaint_description} for complaint in new_complaints]
    return JsonResponse({'new_complaints': data})


# views.py

# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import UserProfile
from django.contrib.auth.hashers import make_password

def reg(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation checks
        if password != confirm_password:
            return render(request, 'reg.html', {'error_message': 'Passwords do not match'})

        # Check if username or email already exists in UserProfile
        if UserProfile.objects.filter(user__username=username).exists():
            return render(request, 'reg.html', {'error_message': 'Username already exists'})
        if UserProfile.objects.filter(email=email).exists():
            return render(request, 'reg.html', {'error_message': 'Email already exists'})

        # Create new user
        User = get_user_model()
        new_user = User.objects.create_user(username=username, email=email, password=password)
        
        # Create UserProfile instance
        user_profile = UserProfile.objects.create(user=new_user, full_name=full_name, phone_number=phone_number)
        
        return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'reg.html')





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BusReservation

@csrf_exempt
def submit_booking_form(request):
    if request.method == 'POST':
        try:
            registration_number = request.POST.get('registration_number')
            full_name = request.POST.get('fullName')
            age = request.POST.get('age')
            phone_number = request.POST.get('phoneNumber')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            selected_seats = request.POST.get('selectedSeats')
            price = request.POST.get('formTotalPrice')

            # Check if all required fields are present
            if not (registration_number and full_name and age and phone_number
                    and email and gender and selected_seats and price):
                return JsonResponse({'error': 'All fields are required'}, status=400)

            # Create BusReservation object and save it
            reservation = BusReservation.objects.create(
                registration_number=registration_number,
                full_name=full_name,
                age=age,
                phone_number=phone_number,
                email=email,
                gender=gender,
                selected_seats=selected_seats,
                price=price
            )

            return JsonResponse({'message': 'Form submitted successfully'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'An error occurred while processing the form'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



from django.shortcuts import render
from .models import Bus

def bus_seat_details(request, bus_id):
    # Retrieve bus details based on the provided bus_id
    bus = Bus.objects.get(pk=bus_id)
    
    # Pass the bus object to the template
    seat_price = SeatPrice.objects.filter(bus_id=bus_id).first()  # Retrieve the seat price for the bus
    return render(request, 'bus_seat_details.html', {'bus': bus, 'seat_price': seat_price})

from django.shortcuts import render, redirect
from .models import Bus, SeatPrice

def bus_seat_price(request):
    if request.method == 'POST':
        bus_id = request.POST.get('bus')
        price = request.POST.get('price')
        
        # Create SeatPrice object and save it
        SeatPrice.objects.create(bus_id=bus_id, price=price)
        
        # Redirect to a success page or any other desired page
        return redirect('admindashboard')  # Replace 'success-page-url' with the actual URL
    
    # If the request method is GET, render the form with the list of registered buses
    buses = Bus.objects.all()
    return render(request, 'bus_seat_price.html', {'buses': buses})