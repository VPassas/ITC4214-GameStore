from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from store.models import Game
from .forms import ProfileForm


def register(request):
    """Register a new user with Django's built in UserCreationForm. On a valid POST it creates the user (password hashed), logs them in, and sends them home. On GET it just shows the empty form."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()       # creates the user and hashes the password
            login(request, user)     # log the new user in immediately
            return redirect("store:home")
    else:
        form = UserCreationForm() # just show the empty form
    return render(request, "accounts/register.html", {"form": form})


@login_required   # only logged in users can reach this page
def dashboard(request):
    """the user's personal dashboard which has the account summary and the games recently viewed."""
    viewed_ids = request.session.get("recently_viewed", [])
    # get the games in one query and then reorder them to be newest first
    games_by_id = {game.id: game for game in Game.objects.filter(id__in=viewed_ids)}
    recently_viewed = [games_by_id[i] for i in viewed_ids if i in games_by_id]
    return render(request, "accounts/dashboard.html", {"recently_viewed": recently_viewed})


@login_required   # only logged in users can reach this page
def profile(request):
    """Show the logged in user's profile and let them update it. Instance=request.user ties the form to THIS user's record."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user) # prepopulate the form with the user's current info
    return render(request, "accounts/profile.html", {"form": form})
