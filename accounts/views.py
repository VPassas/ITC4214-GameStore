from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Register a new user with Django's built-in UserCreationForm.
    On a valid POST it creates the user (password hashed), logs them in,
    and sends them home. On GET it just shows the empty form."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()       # creates the user and hashes the password
            login(request, user)     # log the new user in immediately
            return redirect("store:home")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})
