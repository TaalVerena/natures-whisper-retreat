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

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the reservation.

    Returns:
        HttpResponse: Rendered HTML template with reservation details.
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

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template with a list of reservations and queries.
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
    """
    Delete a reservation if confirmed by the staff user.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the reservation to delete.

    Returns:
        HttpResponse: Redirects to reservation list after deletion or renders confirmation page.
    """
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
    """
    Edit details of an existing reservation by staff.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the reservation to edit.

    Returns:
        HttpResponse: Redirects to reservation list after editing or renders edit form.
    """
    reservation = get_object_or_404(Reservation, pk=pk)

    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)

        if form.is_valid():
            edited_reservation = form.save(commit=False)

            # Check for overlapping reservations (double booking)
            conflicting_reservations = Reservation.objects.filter(
                lodge=edited_reservation.lodge,
                start_date__lt=edited_reservation.end_date,
                end_date__gt=edited_reservation.start_date,
                status=Reservation.Status.CONFIRMED,
            ).exclude(
                pk=pk
            )  # Exclude the current reservation

            if conflicting_reservations.exists():
                messages.error(
                    request, "Selected dates overlap with an existing booking."
                )
            elif edited_reservation.start_date >= edited_reservation.end_date:
                messages.error(request, "Check-out date must be after check-in date.")
            else:
                edited_reservation.save()
                messages.success(request, "Reservation edited successfully.")
                return redirect("reservation_list")
    else:
        form = ReservationForm(instance=reservation)

    return render(
        request,
        "dashboard/edit_reservation.html",
        {"form": form, "reservation": reservation},  # Ensure this context is passed
    )


@login_required
@user_passes_test(is_staff_user)
def change_reservation_status(request, pk):
    """
    Change the status of a reservation by staff.

    Parameters:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the reservation to change status.

    Returns:
        HttpResponse: Redirects to reservation list after status change or renders status form.
    """
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
    """
    Display and update the user's profile information.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to profile after updating or renders profile form.
    """
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "dashboard/profile.html", {"form": form})
