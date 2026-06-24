from django.urls import path
from . import views

# refer to these urls as "store:home" and "store:game_detail"  to avoid name collisions if another app also has a "home" or "game_detail"
app_name = "store"

urlpatterns = [
    path("", views.home, name="home"),
    path("game/<int:id>/", views.game_detail, name="game_detail"),
]
