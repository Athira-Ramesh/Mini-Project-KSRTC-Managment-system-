#models.py
from django.contrib.auth.models import AbstractUser
from django.db import models



        
class Terminal(models.Model):
    terminal_id = models.AutoField(primary_key=True)
    terminal_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)  # New field for confirm password

    def __str__(self):
        return self.terminal_name


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=50)
    posts = models.CharField(max_length=50)
    terminal = models.ForeignKey(Terminal,on_delete=models.CASCADE)  # ForeignKey to Terminal model
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username        
 




    
class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    registration_number = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE,related_name='allocated_bus')
    
    def __str__(self):
        return f'Bus ID: {self.bus_id}, Registration Number: {self.registration_number}, Bus Number: {self.bus_number}, Status: {self.status}, Terminal: {self.terminal.terminal_name}'

     
 





class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=100)
    source_time = models.TimeField()
    destination = models.CharField(max_length=100)
    destination_time = models.TimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,related_name='allocated_route')

    def __str__(self):
        return f'Route {self.route_id}: {self.source} to {self.destination} (Bus: {self.bus.registration_number})'     



class Staff_Allocation(models.Model):
    allocation_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE, related_name='allocated_staff')
    allocation_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.staff.full_name} allocated to {self.terminal.terminal_name}'





class BusAllocation(models.Model):
    allocation_id = models.AutoField(primary_key=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    allocation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Bus ID: {self.bus.bus_id} allocated to Terminal: {self.terminal.terminal_name} on {self.allocation_date}'



class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    bus_allocation = models.ForeignKey(BusAllocation, on_delete=models.CASCADE)
    staff_allocation = models.ForeignKey(Staff_Allocation, on_delete=models.CASCADE)

    def __str__(self):
        return f'Assignment ID: {self.assignment_id}, Bus: {self.bus_allocation.bus.registration_number}, Staff: {self.staff_allocation.staff.full_name}, Terminal: {self.staff_allocation.terminal.terminal_name}'
           




class DailyCollection(models.Model):
    dailycollection_id = models.AutoField(primary_key=True)
    staff_allocation = models.ForeignKey(Staff_Allocation, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    collection_date = models.DateField(auto_now_add=True)
    collection_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def terminal_name(self):
        return self.staff_allocation.terminal.terminal_name

    def bus_allocation(self):
        return self.assignment.bus_allocation.bus

    def __str__(self):
        return f'Daily Collection ID: {self.dailycollection_id}, Staff: {self.staff_allocation.staff.full_name}, Terminal: {self.terminal_name()}, Bus Allocation: {self.bus_allocation()}, Collection Date: {self.collection_date}, Collection Amount: {self.collection_amount}'


class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    staff_allocation = models.ForeignKey(Staff_Allocation, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    complaint_date = models.DateField(auto_now_add=True)
    complaint_description = models.TextField()

    def terminal_name(self):
        return self.staff_allocation.terminal.terminal_name

    def bus_allocation(self):
        return self.assignment.bus_allocation.bus

    def __str__(self):
       return f'Complaint ID: {self.complaint_id}, Staff: {self.staff_allocation.staff.full_name}, Terminal: {self.terminal_name()}, Bus Allocation: {self.bus_allocation()}, Complaint Date: {self.complaint_date}, Complaint Description: {self.complaint_description}'


class ComplaintReply(models.Model):
    replay_id = models.AutoField(primary_key=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    reply_description = models.TextField()

    def __str__(self):
        return f'Reply ID: {self.replay_id}, Complaint ID: {self.complaint.complaint_id}'



class Workshop(models.Model):
    workshop_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)

    def __str__(self):
        return f"Workshop ID: {self.workshop_id}, User Name: {self.user_name}, Location: {self.location}"



class WorkshopComplaint(models.Model):
    workshop_complaint_id = models.AutoField(primary_key=True)
    complaint_description = models.TextField()
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    latitude = models.FloatField()  # Latitude field
    longitude = models.FloatField()  # Longitude field


    def __str__(self):
        return f"Workshop Complaint ID: {self.workshop_complaint_id}"



class ComplaintResponse(models.Model):
    complaint_response_id = models.AutoField(primary_key=True)
    workshop_complaint = models.ForeignKey(WorkshopComplaint, on_delete=models.CASCADE)
    response_description = models.TextField()



    def save(self, *args, **kwargs):
        self.workshop_complaint.response_submitted = True  # Mark response submitted
        self.workshop_complaint.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Complaint Response ID: {self.complaint_response_id}"       



# models.py
from django.db import models
from django.conf import settings

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)




from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.full_name




from django.db import models

class BusReservation(models.Model):
    registration_number = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    selected_seats = models.CharField(max_length=200)  # Assuming seat numbers will be stored as a string
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Adding a price field

    def __str__(self):
        return f"Bus Reservation - {self.full_name}"     
