from django.shortcuts import render
from .models import Game


def home(request):
    """the home page, which shows all the games in the store"""
    games = Game.objects.all()
    return render(request, "store/home.html", {"games": games})
