from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from reservations.models import Reservation
from .forms import ReservationForm
from contact.models import ContactRequest
from contact.forms import ContactForm
from django.contrib.auth.models import User
from .forms import ProfileForm


def is_staff_user(user):
    """
    Check if the user is staff.
    """
    return user.is_staff


@login_required
def dashboard(request):
    """
    Render user reservations and contact form.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template for the user dashboard.
    """
    user = request.user
    current_date = datetime.now().date()

    # Include all statuses for upcoming reservations
    upcoming_reservations = Reservation.objects.filter(
        user=user, start_date__gte=current_date
    ).order_by("start_date")

    past_reservations = Reservation.objects.filter(
        user=user, start_date__lt=current_date, status=Reservation.Status.CONFIRMED
    ).order_by("-start_date")

    user_contact_requests = ContactRequest.objects.filter(user=user).order_by(
        "-created_at"
    )

    contact_form = ContactForm()

    context = {
        "upcoming_reservations": upcoming_reservations,
        "past_reservations": past_reservations,
        "contact_form": contact_form,
        "user_contact_requests": user_contact_requests,
    }

    return render(request, "dashboard/dashboard.html", context)


@login_required
@user_passes_test(is_staff_user)
def view_reservation(request, pk):
    """
    Display the details of a reservation with options to edit, delete, or cancel.
    """
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(
        request, "dashboard/view_reservation.html", {"reservation": reservation}
    )


@login_required
@user_passes_test(is_staff_user)
def reservation_list(request):
    """
    Display a list of reservations and user queries for staff users.
    """
    current_date = datetime.now().date()

    # Fetch upcoming reservations (starting today or in the future)
    upcoming_reservations = Reservation.objects.filter(
        start_date__gte=current_date
    ).order_by("start_date")

    # Fetch past reservations (started before today)
    past_reservations = Reservation.objects.filter(
        start_date__lt=current_date
    ).order_by("-start_date")

    # Fetch all user queries
    user_queries = ContactRequest.objects.all().order_by("-created_at")

    return render(
        request,
        "dashboard/reservation_list.html",
        {
            "upcoming_reservations": upcoming_reservations,
            "past_reservations": past_reservations,
            "user_queries": user_queries,
        },
    )


@login_required
@user_passes_test(is_staff_user)
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == "POST":
        reservation.delete()
        messages.success(request, "Reservation deleted successfully.")
        return redirect("reservation_list")

    return render(
        request, "dashboard/delete_reservation.html", {"reservation": reservation}
    )


@login_required
@user_passes_test(is_staff_user)
def edit_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation edited successfully.")
            return redirect("reservation_list")
    else:
        form = ReservationForm(instance=reservation)
    return render(request, "dashboard/edit_reservation.html", {"form": form})


@login_required
@user_passes_test(is_staff_user)
def change_reservation_status(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.method == "POST":
        form = ChangeStatusForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation status changed successfully.")
            return redirect("reservation_list")
    else:
        form = ChangeStatusForm(instance=reservation)
    return render(request, "dashboard/change_status.html", {"form": form})


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "dashboard/profile.html", {"form": form})
