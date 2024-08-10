from django.shortcuts import render


def about_view(request):
    """
    Render the 'about' page template.
    """
    return render(request, "about/about.html")
