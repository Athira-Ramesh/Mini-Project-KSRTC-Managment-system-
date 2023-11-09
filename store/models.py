#models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

 
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=50)
    posts = models.CharField(max_length=50)
    terminal = models.CharField(max_length=50) # Add any additional fields you need

    def __str__(self):
        return self.username       


class Terminal(models.Model):
    terminal_id = models.AutoField(primary_key=True)
    terminal_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    





    
class Bus(models.Model):
    bus_id = models.AutoField(primary_key=True)
    registration_number = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)

    def __str__(self):
        return f'Bus ID: {self.bus_id}, Registration Number: {self.registration_number}, Bus Number: {self.bus_number}, Status: {self.status}, Terminal: {self.terminal.terminal_name}'
 





class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=100)
    source_time = models.TimeField()
    destination = models.CharField(max_length=100)
    destination_time = models.TimeField()
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)

    def __str__(self):
        return f'Route {self.route_id}: {self.source} to {self.destination} (Bus: {self.bus.registration_number})'     



class Staff_Allocation(models.Model):
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    terminal = models.ForeignKey(Terminal, on_delete=models.CASCADE)
    allocation_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.staff.full_name} allocated to {self.terminal.terminal_name}'

        
           
