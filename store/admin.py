from django.contrib import admin
from .models import Category, Game, Rating, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    # columns shown in the games list
    list_display = ("title", "category", "platform", "price", "stock")
    # sidebar filters
    list_filter = ("category", "platform")
    # search box for title
    search_fields = ("title",)

# here we register the Rating and Like models with the admin site so we can see them in the admin panel. We also customize the list display and filters for each model.
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "score", "created_at")
    list_filter = ("score",)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "game", "created_at")
