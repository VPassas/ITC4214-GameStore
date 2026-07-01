from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Game, Category, Rating, Like


def home(request):
    """the home page gets all games and passes them to the template"""
    games = Game.objects.all()
    return render(request, "store/home.html", {"games": games})


def game_detail(request, id):
    """this shows the details of a single game and sends 404 if the id does not exist"""
    game = get_object_or_404(Game, id=id)

    # remember this game in the user's session so the dashboard can show "recently viewed"
    viewed = request.session.get("recently_viewed", [])  # list of game ids or empty list the first time
    if id in viewed:
        viewed.remove(id)            # if already seen take it out so we can move it to the front
    viewed.insert(0, id)             # newest viewed goes first
    request.session["recently_viewed"] = viewed[:6]  # keep only the 6 most recent

    summary = _rating_summary(game)
    # what has this user already done with this game
    user_score = 0
    user_liked = False
    if request.user.is_authenticated:
        rating = game.ratings.filter(user=request.user).first()
        user_score = rating.score if rating else 0
        user_liked = game.likes.filter(user=request.user).exists()

    context = {
        "game": game,
        "average": summary["average"],
        "rating_count": summary["count"],
        "user_score": user_score,
        "like_count": game.likes.count(),
        "user_liked": user_liked,
    }
    return render(request, "store/game_detail.html", context)


def _rating_summary(game):
    """average score rounded and number of ratings for a game. Shared by game_detail and rate so we do not repeat the query"""
    avg = game.ratings.aggregate(avg=Avg("score"))["avg"]  # none if no ratings yet
    return {"average": round(avg, 1) if avg else 0, "count": game.ratings.count()}


@login_required
@require_POST
def rate(request, id):
    """an AJAX endpoint where we save or update the current user's 1-5 rating for a game and return the new average"""
    game = get_object_or_404(Game, id=id)
    try:
        score = int(request.POST.get("score", 0))
    except ValueError:
        score = 0
    if score < 1 or score > 5:
        return JsonResponse({"error": "Score must be 1-5"}, status=400)

    # update the user's existing rating or create one if this is their first
    Rating.objects.update_or_create(user=request.user, game=game, defaults={"score": score})

    summary = _rating_summary(game)
    return JsonResponse({"average": summary["average"], "count": summary["count"], "user_score": score})


@login_required
@require_POST
def toggle_like(request, id):
    """another AJAX endpoint where the user can like the game if not liked yet, otherwise unlike it and return the new like state and count"""
    game = get_object_or_404(Game, id=id)
    like, created = Like.objects.get_or_create(user=request.user, game=game)
    if not created:       # it already existed therefore this click means "unlike"
        like.delete()
    return JsonResponse({"liked": created, "count": game.likes.count()})


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
