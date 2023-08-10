from django.db import models
from django.utils.timezone import now
from site_admin.models import Location, Category
# Create your models here.
class Registration(models.Model):
    unique_id=models.AutoField(primary_key=True, null=False)
    firstname = models.CharField(max_length=100, default='null', null=False)
    lastname = models.CharField(max_length=100, default='null', null=False)
    email = models.CharField(max_length=255, default='null', null=False)
    password = models.CharField(max_length=500, default='null', null=False)
    mobilenumber = models.CharField(max_length=15, default='null', null=False)
    address = models.TextField(default='null', null=False )
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    about_me = models.TextField(default='null', null=False )
    my_skills = models.TextField(default='null', null=False )
    profile_image = models.TextField(blank=True, null=True)     
    status_choices = [
        ('pending', 'Pending'),
        ('active', 'Active'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default="active")
    date_added = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.email
