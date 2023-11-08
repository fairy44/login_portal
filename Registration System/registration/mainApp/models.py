from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
class Users(models.Model):
    Username=models.CharField(max_length=50)
    First_name=models.CharField(max_length=50)
    Last_name=models.CharField(max_length=50)
    Password=models.CharField(max_length=50)
    Email_Address = models.EmailField(max_length=50, unique=True, default='')

class TimeHistory(models.Model):       
    Username = models.CharField(max_length=50, null=True)
    Password=models.CharField(max_length=50)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    login_method = models.CharField(null=True, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) 
    google_id = models.CharField(max_length=255, null=True, blank=True)


# class CustomUser(AbstractUser):
#     authentication_source = models.CharField(max_length=10, null=True, blank=True)


    # Add any other fields you need for the user's profile

    def __str__(self):
        return self.user.username
    def set_login_time(self):
        self.login_time = timezone.now()
        self.save()

    def set_logout_time(self):
        self.logout_time = timezone.now()
        self.save()
   

class TimeHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming a ForeignKey relationship with the User model
    google_id = models.CharField(max_length=255, blank=True, null=True)
    Username = models.CharField(max_length=50, null=True)
    Password = models.CharField(max_length=50)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    login_method = models.CharField(null=True, max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    google_id = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.user.username

    def set_login_time(self):
        self.login_time = timezone.now()
        self.save()

    def set_logout_time(self):
        self.logout_time = timezone.now()
        self.save()
