from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from mainApp.models import Users, TimeHistory
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import TimeHistory
from social_django.utils import load_strategy
from allauth.socialaccount.models import SocialAccount
from social_django.models import UserSocialAuth 
from django.shortcuts import render
from social.apps.django_app.default.models import UserSocialAuth
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from mainApp.models import TimeHistory


#@login_required(login_url='login')
def Home(request):
    user = request.user
    userdata = Users.objects.all()
    timedata = TimeHistory.objects.all()
    is_google_user = False  # Default to False

    # Check if the user is authenticated and has a Google social account
    if request.user.is_authenticated:
        # You need to modify this logic based on how you've integrated Google login
        # If you're using django-allauth, you can use something like this:
        if request.user.socialaccount_set.filter(provider='google').exists():
            is_google_user = True
            
    
    data = {
        'userdata': userdata,
        'timedata': timedata,
        'is_google_user': is_google_user
        
    
    }
    print(data)
    return render(request, 'home.html', data)


def SignupPage(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 != pass2:
            return HttpResponse("your password and confirm password doesn't match")

        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()

            new_Login_history = Users(
                Username=username, First_name=fname, Last_name=lname, Password=pass1, Email_Address=email)
            new_Login_history.save()

            return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)
        if user is not None:
            # login(request, user)
            # content = request.environ['wsgi.input'].read()
            # content_string = content.decode('utf-8')  

            # raise ValidationError(user)
            # Create a new TimeHistory instance
            time_history = TimeHistory(
                    Username=username, Password=password,login_method='user',)
            time_history.set_login_time()  # Set the login time
            time_history.set_logout_time()
            time_history.save()
            request.session['login_time'] = str(timezone.now())
            request.session['logout_time'] = str(timezone.now())
            #next_url = request.GET.get('next', 'home')
            #print(next_url)
            print(f"User {user.username} logged in successfully.")
            return redirect('Home')
            
        else:
            return HttpResponse("Username or password is incorrect")

    return render(request, 'login.html')


"""def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')
        user = authenticate(username=username, password=password)
        return redirect('Home')
    
    
    return render(request,'login.html')
       """
   

            
        


def LogoutPage(request):
    if request.user.is_authenticated:
        custom_user = TimeHistory.objects.get(username=request.user.username)
        custom_user.set_logout_time()
    logout(request)
    return redirect('login')


def LogoutPage(request):
    if request.user.is_authenticated:
        try:
            # Get all TimeHistory entries associated with the user
            time_history_entries = TimeHistory.objects.filter(Username=request.user.username)

            # Update the logout time for each entry
            for time_history in time_history_entries:
                time_history.set_logout_time()
                time_history.save()

        except TimeHistory.DoesNotExist:
            pass  # User's TimeHistory entry doesn't exist, do nothing

        logout(request)

    return redirect('login')


def LogoutPage(request):
    if request.user.is_authenticated:
        try:
            # Get all TimeHistory entries associated with the user
            time_history_entries = TimeHistory.objects.filter(
                Username=request.user.username)

            # Update the logout time for each entry
            for time_history in time_history_entries:
                if not time_history.logout_time:  # Update only if logout time is not set
                    time_history.set_logout_time()
                    time_history.save()

        except ObjectDoesNotExist:
            pass  # User's TimeHistory entry doesn't exist, do nothing

        logout(request)

    return redirect('login')


def social_auth_data(request):
    social_auth_entries = UserSocialAuth.objects.all()  # Query all records from the social_auth_usersocialauth table
    return render(request, 'social_auth_data.html', {'social_auth_entries': social_auth_entries})



    