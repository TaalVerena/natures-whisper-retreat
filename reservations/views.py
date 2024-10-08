from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from datetime import date, timedelta
from .forms import ReservationForm
from lodges.models import Lodge
from django.utils import timezone
from .models import Reservation


@login_required
def make_reservation(request, lodge_id):
    """
    Handle the creation of a reservation for a specific lodge.
    """
    lodge = get_object_or_404(Lodge, pk=lodge_id)
    form = ReservationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        reservation = form.save(commit=False)
        reservation.lodge = lodge
        reservation.user = request.user
        reservation.status = Reservation.Status.PENDING

        # Calculate total nights of the reservation
        reservation.total_nights = (reservation.end_date - reservation.start_date).days

        # Ensure start date is not today or in the past
        if reservation.start_date <= date.today():
            messages.error(request, "Start date cannot be today or in the past.")
            return render(
                request,
                "reservations/make_reservation.html",
                {"form": form, "lodge": lodge},
            )

        # Calculate total cost based on lodge's rate and duration
        if reservation.total_nights > 0:
            reservation.total_cost = lodge.rate * reservation.total_nights
        else:
            messages.error(request, "Check-out date must be after check-in date.")
            return render(
                request,
                "reservations/make_reservation.html",
                {"form": form, "lodge": lodge},
            )

        # Check for overlapping reservations (double booking)
        conflicting_reservations = Reservation.objects.filter(
            lodge=lodge,
            start_date__lt=reservation.end_date,
            end_date__gt=reservation.start_date,
            status=Reservation.Status.CONFIRMED,
        )

        if conflicting_reservations.exists():
            messages.error(request, "Selected dates overlap with an existing booking.")
            return render(
                request,
                "reservations/make_reservation.html",
                {"form": form, "lodge": lodge},
            )

        reservation.save() # Save the reservation if no conflicts
        messages.success(
            request, "Your reservation has been submitted and is pending confirmation."
        )
        return redirect("reservation_confirmation", reservation_id=reservation.id)

    return render(
        request, "reservations/make_reservation.html", {"form": form, "lodge": lodge}
    )


@login_required
def reservation_confirmation(request, reservation_id):
    """
    View to handle the confirmation and cancellation of reservations.

    Parameters:
        request (HttpRequest): The HTTP request object.
        reservation_id (int): The primary key of the reservation to be confirmed or cancelled.

    Returns:
        HttpResponse: Renders the confirmation page or redirects upon action.
    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.user != request.user:
        messages.error(request, "You do not have permission to view this reservation.")
        return redirect("dashboard")

    previous_url = request.META.get("HTTP_REFERER", "/")
    today = timezone.now().date()

    # Check if the reservation can be edited or canceled
    is_editable = (
        reservation.status != Reservation.Status.CANCELLED
        and reservation.start_date > today
    )

    if request.method == "POST":
        if is_editable:
            if "confirm" in request.POST:
                reservation.status = Reservation.Status.CONFIRMED
                reservation.save()
                messages.success(request, "Reservation confirmed!")
                print("Debug: Reservation confirmed.")
                return redirect("dashboard")
            elif "cancel" in request.POST:
                reservation.status = Reservation.Status.CANCELLED
                reservation.save()
                messages.info(request, "Reservation cancelled.")
                print("Debug: Reservation cancelled.")
                return redirect("dashboard")
        else:
            messages.error(request, "This reservation cannot be edited or cancelled.")
            print("Debug: Attempted to edit or cancel a non-editable reservation.")
            return redirect("dashboard")

    context = {
        "reservation": reservation,
        "is_editable": is_editable,
        "previous_url": previous_url,
    }

    return render(request, "reservations/reservation_confirmation.html", context)


def get_booked_dates(request, lodge_id):
    """
    Fetch booked dates for a lodge, including pending reservations.

    Parameters:
        request (HttpRequest): The request object.
        lodge_id (int): The ID of the lodge.

    Returns:
        JsonResponse: JSON response with booked dates.
    """
    today = date.today()
    reservations = Reservation.objects.filter(
        lodge_id=lodge_id,
        end_date__gte=today,
        status__in=[
            Reservation.Status.CONFIRMED,
            Reservation.Status.PENDING,
        ],
    )
    booked_dates = []

    # Compile all booked dates within each reservation period
    for reservation in reservations:
        current_date = reservation.start_date
        while current_date <= reservation.end_date:
            booked_dates.append(current_date.strftime("%Y-%m-%d"))
            current_date += timedelta(days=1)

    return JsonResponse(booked_dates, safe=False)
