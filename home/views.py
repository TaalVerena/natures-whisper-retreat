from django.shortcuts import render
from .models import LodgeOverview


def home_view(request):
    """
    View function for rendering the home page.

    Retrieves all LodgeOverview objects from the
    database and renders the 'index.html' template
    with the retrieved lodges data.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered response containing
        the home page with lodge data.
    """
    lodges = LodgeOverview.objects.all()
    return render(request, 'home/index.html', {'lodges': lodges})
