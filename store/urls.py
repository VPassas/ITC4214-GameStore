from django.urls import path
from . import views

# refer to these urls as "store:home" to avoid name collisions with other apps
app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("game/<int:id>/", views.game_detail, name="game_detail"),
    path("category/<int:id>/", views.category_games, name="category_games"),
]
