from .models import Category

def categories_processor(request):
    """
    Context processor to make categories available in all templates.
    """
    return {
        'categories': Category.objects.all()
    } 