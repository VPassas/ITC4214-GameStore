from django.shortcuts import render, get_object_or_404
from .models import Game


def home(request):
    """the homepage gets all the games and sends them to the template"""
    games = Game.objects.all()
    return render(request, "store/home.html", {"games": games})


def game_detail(request, id):
    """this shows the details of a single game, identified by its id"""
    game = get_object_or_404(Game, id=id)
    return render(request, "store/game_detail.html", {"game": game})
