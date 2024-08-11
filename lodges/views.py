from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Lodge
from .forms import LodgeForm


def is_staff_user(user):
    """
    Check if the user is staff.
    """
    return user.is_staff


def lodge_list(request):
    """
    Display a paginated list of lodges.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template displaying a list of lodges.
    """
    lodges_list = Lodge.objects.all().order_by("name")
    paginator = Paginator(lodges_list, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "lodges/lodge_list.html", {"page_obj": page_obj})


def lodge_detail(request, pk):
    """
    Display details of a single lodge.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the lodge.

    Returns:
        HttpResponse: Rendered HTML template displaying lodge details.
    """
    lodge = get_object_or_404(Lodge, pk=pk)
    return render(request, "lodges/lodge_detail.html", {"lodge": lodge})


@login_required
def add_lodge(request):
    """
    Add a new lodge.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to lodge list on success or renders form template on failure.
    """
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")

    if request.method == "POST":
        form = LodgeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Lodge added successfully.")
            return redirect("lodges")
    else:
        form = LodgeForm()
    return render(request, "lodges/lodge_form.html", {"form": form})


@login_required
def edit_lodge(request, pk):
    """
    Edit an existing lodge.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the lodge to edit.

    Returns:
        HttpResponse: Redirects to lodge list on success or renders form template on failure.
    """
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")

    lodge = get_object_or_404(Lodge, pk=pk)
    if request.method == "POST":
        form = LodgeForm(request.POST, request.FILES, instance=lodge)
        if form.is_valid():
            form.save()
            messages.success(request, "Lodge updated successfully.")
            return redirect("lodges")
    else:
        form = LodgeForm(instance=lodge)
    return render(request, "lodges/lodge_form.html", {"form": form})


@login_required
def delete_lodge(request, pk):
    """
    Delete an existing lodge.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the lodge to delete.

    Returns:
        HttpResponse: Redirects to lodge list on success or renders confirmation template.
    """
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect("home")

    lodge = get_object_or_404(Lodge, pk=pk)
    if request.method == "POST":
        lodge.delete()
        messages.success(request, "Lodge deleted successfully.")
        return redirect("lodges")
    return render(request, "lodges/lodge_confirm_delete.html", {"lodge": lodge})
