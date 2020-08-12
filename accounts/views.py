from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        return render(request, "home.html")


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Username or password is incorrect.')
            return redirect('')
    else:
        return render(request, '')
