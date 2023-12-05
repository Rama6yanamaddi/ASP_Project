from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.forms import UserLoginForm, UserRegistrationForm
from accounts.models import LoginLog

from collections import namedtuple
from datetime import datetime

# Order line items rendering view type
OrderView = namedtuple('OrderView',
                       ['order_date',
                        'days',
                        'vehicle_image',
                        'vehicle_model',
                        'from_date',
                        'to_date',
                        'subtotal'])


# View rendering terms and conditions page
def terms(request):
    """
    Return the terms.html
    """
    return render(request, 'terms.html')

# Logout user and redirect to index page
@login_required
def logout(request):
    """
    Log the user out
    """
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('index'))


# Endpoint to login user
def login(request):
    """
    Return the login page
    """
    # If user is already authenticated, redirect to homepage
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            if user:
                auth.login(user=user, request=request)
                login_log = LoginLog(user=user)
                login_log.save()
                messages.success(request, "You have successfully logged in!")
                return redirect(reverse('index'))
            else:
                login_form.add_error(
                    None, "Your username or password is incorrect")
    else:
        # If it is get request, create new login form to be rendered
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})

# Handle user registration 
def registration(request):
    """
    Render the registration form page
    """
    # Authenticated users are registered for sure so get homepage
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered!")
                return redirect(reverse('index'))
            else:
                messages.error(
                    request, "Unable to register your account at this time")

    else:
        # If it is get, create new form instance to be rendered
        registration_form = UserRegistrationForm()

    return render(
        request, 'registration.html', {
            "registration_form": registration_form})


 
