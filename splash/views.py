from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group

def splash(request):
       if request.user.is_authenticated:
              return render(request, "splash.html")
       else:
              return redirect('/')


def logout(request):
    auth.logout(request);
    return redirect('/')

