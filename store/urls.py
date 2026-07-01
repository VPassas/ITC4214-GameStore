from django.urls import path
from . import views

# refer to these urls as "store:home" to avoid name collisions with other apps
app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("game/<int:id>/", views.game_detail, name="game_detail"),
    path("game/<int:id>/rate/", views.rate, name="rate"),
    path("game/<int:id>/like/", views.toggle_like, name="toggle_like"),
    path("category/<int:id>/", views.category_games, name="category_games"),
]
