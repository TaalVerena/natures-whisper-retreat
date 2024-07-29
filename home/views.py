from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LodgeOverview
from .forms import LodgeOverviewForm


def home_view(request):
    """
    View function for rendering the home page.
    Retrieves all LodgeOverview objects from the database and renders the 'index.html' template
    with the retrieved lodges data.
    """
    lodges = LodgeOverview.objects.all()
    return render(request, "home/index.html", {"lodges": lodges})


@login_required
def edit_lodge_overview(request, pk):
    """
    Edit an existing lodge overview.
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
