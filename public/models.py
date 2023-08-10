from django.db import models
from django.utils.timezone import now
from mechanic.models import Registration as Mechanic_Registartion

# Create your models here.
class Registration(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    firstname = models.CharField(max_length=100, default='null', null=False)
    lastname = models.CharField(max_length=100, default='null', null=False)
    email = models.CharField(max_length=255, default='null', null=False)
    password = models.CharField(max_length=500, default='null', null=False)
    mobilenumber = models.CharField(max_length=15, default='null', null=False)
    address = models.TextField(default='null', null=False)
    status_choices = [
        ('pending', 'Pending'),
        ('active', 'Active'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default="active")
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.email

class Complaints(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    complaints_text=models.TextField(default='null', null=False)
    location_text=models.TextField(default='null', null=False)
    selected_mechanic = models.ForeignKey(Mechanic_Registartion, on_delete=models.CASCADE)
    public_user = models.ForeignKey(Registration, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=now, editable=False)
    reply = models.TextField(default='null', null=True)
    status_choices = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default="open")

    def __str__(self):
        return self.complaints_subject

class Messages(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    complaints=models.ForeignKey(Complaints, on_delete=models.CASCADE)
    mechanic_user_id=models.IntegerField(default=0)
    public_user_id = models.IntegerField(default=0)
    messages_text=models.TextField(default='null', null=False)
    date_added = models.DateTimeField(default=now, editable=False)
    status_choices = [
        ('mechanic_user', 'Mechanic User'),
        ('user', 'User'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default="user")

    def __str__(self):
        return self.messages_text
