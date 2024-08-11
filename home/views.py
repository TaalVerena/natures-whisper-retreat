from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LodgeOverview
from .forms import LodgeOverviewForm


def home_view(request):
    """
    Render the home page with a list of all lodges.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered 'index.html' template with all lodges.
    """
    lodges = LodgeOverview.objects.all()
    return render(request, "home/index.html", {"lodges": lodges})


@login_required
def edit_lodge_overview(request, pk):
    """
    Edit an existing lodge overview.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the lodge overview to edit.

    Returns:
        HttpResponse: The rendered form for editing a lodge overview,
                      or a redirect to the home page upon successful submission.
    """
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")

    lodge = get_object_or_404(LodgeOverview, pk=pk)
    if request.method == "POST":
        form = LodgeOverviewForm(request.POST, request.FILES, instance=lodge)
        if form.is_valid():
            form.save()
            messages.success(request, "Lodge overview updated successfully.")
            return redirect("home")
    else:
        form = LodgeOverviewForm(instance=lodge)
    return render(request, "home/lodge_overview_form.html", {"form": form})
