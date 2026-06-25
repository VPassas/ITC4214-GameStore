from django.shortcuts import render, get_object_or_404
from django.db.models import Q
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


def search(request):
    """Search games by title and or description and apply filters (category, platform, price range). This works by reading the options from the URL (GET)"""
    games = Game.objects.all()

    # read the search box and filters from the URL query string (?q=...&category=...)
    q = request.GET.get("q", "")
    category_id = request.GET.get("category", "")
    platform = request.GET.get("platform", "")
    min_price = request.GET.get("min_price", "")
    max_price = request.GET.get("max_price", "")

    # apply each filter if the user actually provided it
    if q:
        # either the title or description contains the query
        games = games.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category_id:
        games = games.filter(category_id=category_id)
    if platform:
        games = games.filter(platform=platform)
    if min_price:
        games = games.filter(price__gte=min_price)   # gte = greater than or equal
    if max_price:
        games = games.filter(price__lte=max_price)   # lte = less than or equal

    context = {
        "games": games,
        "platforms": Game.PLATFORM_CHOICES,
        # send the chosen values back so the form stays filled in
        "q": q,
        "selected_category": category_id,
        "selected_platform": platform,
        "min_price": min_price,
        "max_price": max_price,
    }
    return render(request, "store/search.html", context)
