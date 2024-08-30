from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import logging as log
import time

def custom_login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            messages.success(request, "Login Successful.")
            # Log the user in
            login(request, user)
            return redirect('/dashboard')  # Redirect to the homepage or dashboard
        else:
            # Invalid login
            messages.error(request, "Invalid email or password.")
            log.error("Invalid login attempt with email: %s", email)
            
            return render(request, 'registration/login.html', {'messages': messages.get_messages(request)})
    
    return render(request, 'registration/login.html')  # Render the login page on GET request

