from django.contrib import admin
from .models import Category, Game


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
