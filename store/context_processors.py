from .models import Category


def categories(request):
    """base.html needs to know about all categories, since the navbar is shared we cannot have view for it, instead, this contest processor was created to pass the categories to all templates"""
    return {"categories": Category.objects.all()}
