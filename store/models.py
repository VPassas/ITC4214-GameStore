from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """A game category, e.g. Action, RPG, Sports."""
    name = models.CharField(max_length=100)

    class Meta:
        # without this the admin would see "Categorys", due to how Django makes words plural by itself
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Game(models.Model):
    """A game sold in the store (one catalogue item)."""

    # dropdown menu for platform options in the admin panel
    PLATFORM_CHOICES = [
        ("PC", "PC"),
        ("PS5", "PlayStation 5"),
        ("Xbox", "Xbox Series X|S"),
        ("Switch", "Nintendo Switch"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default="PC")
    # each game belongs to a category and if the category is deleted its games go too
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="games"
    )
    image = models.ImageField(upload_to="games/", blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    """a user's star rating out of 5 for one game."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveSmallIntegerField()  # we only ever store 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # a user can only have one rating per game and rating again updates the old one
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user.username} rated {self.game.title}: {self.score}"


class Like(models.Model):
    """ a user 'liking' a game. The row existing means they like it if there is no row means they do not"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # a user can only like a game once
        unique_together = ("user", "game")

    def __str__(self):
        return f"{self.user.username} likes {self.game.title}"
