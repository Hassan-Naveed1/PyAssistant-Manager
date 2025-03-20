from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('host_list')
        else:
            print(form.errors)  # ✅ Debugging line to check errors
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


    return render(request, 'users/register.html', {'form': form})
def login_view(request):
    """Handles user login and redirects to hosts page after login."""
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('host_list')  # ✅ Redirect to hosts page after login
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    return redirect('login')
