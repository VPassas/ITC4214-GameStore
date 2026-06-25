from django.shortcuts import render, get_object_or_404
from .models import Game, Category


def home(request):
    """the home page gets all games and passes them to the template"""
    games = Game.objects.all()
    return render(request, "store/home.html", {"games": games})


def game_detail(request, id):
    """this shows the details of a single game and sends 404 if the id does not exist"""
    game = get_object_or_404(Game, id=id)
    return render(request, "store/game_detail.html", {"game": game})


def category_games(request, id):
    """show all games in one category"""
    category = get_object_or_404(Category, id=id)
    games = category.games.all()  # uses related_name="games" on the ForeignKey
    return render(request, "store/category.html", {"category": category, "games": games})
