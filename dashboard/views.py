from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from reservations.models import Reservation
from .forms import ReservationForm, ChangeStatusForm
from contact.forms import ContactForm


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

    upcoming_reservations = Reservation.objects.filter(
        user=user, start_date__gte=current_date, status=Reservation.Status.CONFIRMED
    ).order_by("start_date")

    past_reservations = Reservation.objects.filter(
        user=user, start_date__lt=current_date, status=Reservation.Status.CONFIRMED
    ).order_by("-start_date")

    contact_form = ContactForm()

    context = {
        "upcoming_reservations": upcoming_reservations,
        "past_reservations": past_reservations,
        "contact_form": contact_form,
    }

    return render(request, "dashboard/dashboard.html", context)


@login_required
@user_passes_test(is_staff_user)
def reservation_list(request):
    """
    Display a list of reservations for staff users, categorized as upcoming or past.
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

    return render(
        request,
        "dashboard/reservation_list.html",
        {
            "upcoming_reservations": upcoming_reservations,
            "past_reservations": past_reservations,
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
            return redirect("reservation_list")
    else:
        form = ChangeStatusForm(instance=reservation)
    return render(request, "dashboard/change_status.html", {"form": form})
