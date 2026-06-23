from django.db import models


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
