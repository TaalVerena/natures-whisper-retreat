from django.shortcuts import render

# Create your views here.
def about_view(request):
    """
    Renders the about page.

    """
    return render(request, 'about/about.html')
