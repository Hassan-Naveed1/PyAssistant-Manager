from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# Here I am handling user registration and logging them in automatically
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('host_list')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

# Here I am handling user login and redirecting to the dashboard if successful
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('host_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# Here I am logging out the user and sending them back to the login page
def logout_view(request):
    logout(request)
    return redirect('login')
