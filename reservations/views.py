from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from .forms import ReservationForm
from lodges.models import Lodge
from .models import Reservation
from datetime import datetime, date, timedelta


@login_required
def make_reservation(request, lodge_id):
    """
    View for making a reservation for a lodge.

    Args:
        request (HttpRequest): The request object.
        lodge_id (int): The ID of the lodge for which reservation is to be made.

    Returns:
        HttpResponse: Renders 'reservations/make_reservation.html' template with reservation form and lodge details.

    """
    lodge = get_object_or_404(Lodge, pk=lodge_id)
    form = ReservationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        reservation = form.save(commit=False)
        reservation.lodge = lodge
        reservation.user = request.user
        reservation.status = Reservation.Status.PENDING

        # Calculate total nights
        reservation.total_nights = (reservation.end_date - reservation.start_date).days

        # Calculate total cost based on lodge's rate
        if reservation.total_nights > 0:
            reservation.total_cost = lodge.rate * reservation.total_nights
        else:
            messages.error(request, "Check-out date must be after check-in date.")
            return render(request, "reservations/make_reservation.html", {"form": form, "lodge": lodge})

        reservation.save()
        return redirect("reservation_confirmation", reservation_id=reservation.id)

    return render(request, "reservations/make_reservation.html", {"form": form, "lodge": lodge})


def reservation_confirmation(request, reservation_id):
    """
    View for confirming or cancelling a reservation.

    Args:
        request (HttpRequest): The request object.
        reservation_id (int): The ID of the reservation.

    Returns:
        HttpResponse: Renders 'reservations/reservation_confirmation.html' template with reservation details.

    """
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            reservation.status = Reservation.Status.CONFIRMED
            reservation.save()
            messages.success(request, "Reservation confirmed!")
            return redirect('home')
        elif 'cancel' in request.POST:
            reservation.status = Reservation.Status.CANCELLED
            reservation.save()
            messages.info(request, "Reservation cancelled.")
            return redirect('home')

    return render(request, 'reservations/reservation_confirmation.html', {'reservation': reservation})


def calendar_events(request, lodge_id):
    """
    View for fetching calendar events for a lodge.

    Args:
        request (HttpRequest): The request object.
        lodge_id (int): The ID of the lodge.

    Returns:
        JsonResponse: JSON response with booked dates and available rates for the lodge.

    """
    lodge = get_object_or_404(Lodge, pk=lodge_id)
    start_date = date.today()
    end_date = start_date + timedelta(days=90)

    reservations = Reservation.objects.filter(
        lodge_id=lodge_id, start_date__lte=end_date, end_date__gte=start_date, status=Reservation.Status.CONFIRMED
    )

    booked_dates = set()
    for reservation in reservations:
        delta = reservation.end_date - reservation.start_date
        for i in range(delta.days + 1):
            day = reservation.start_date + timedelta(days=i)
            booked_dates.add(day.strftime("%Y-%m-%d"))

    events = []
    for day in booked_dates:
        events.append(
            {
                "title": "Fully Booked",
                "start": day,
                "end": day,
                "color": "#ff9f89",
                "textColor": "#000000",
                "allDay": True,
                "type": "booked",
            }
        )

    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime("%Y-%m-%d") not in booked_dates:
            events.append(
                {
                    "title": f"Rate: ${lodge.rate}",
                    "start": current_date.strftime("%Y-%m-%d"),
                    "end": current_date.strftime("%Y-%m-%d"),
                    "color": "#ccffcc",
                    "textColor": "#000000",
                    "allDay": True,
                    "type": "rate",
                }
            )
        current_date += timedelta(days=1)

    return JsonResponse(events, safe=False)


def get_booked_dates(request, lodge_id):
    """
    View for fetching booked dates for a lodge.

    Args:
        request (HttpRequest): The request object.
        lodge_id (int): The ID of the lodge.

    Returns:
        JsonResponse: JSON response with booked dates and their statuses.

    """
    today = datetime.today()
    end_date = today + timedelta(days=90)

    reservations = Reservation.objects.filter(
        lodge_id=lodge_id, start_date__lte=end_date, end_date__gte=today
    )
    booked_dates = []

    for reservation in reservations:
        delta = reservation.end_date - reservation.start_date
        for i in range(delta.days + 1):
            date = reservation.start_date + timedelta(days=i)
            booked_dates.append({
                'date': date.strftime('%Y-%m-%d'),
                'status': reservation.status
            })

    return JsonResponse(booked_dates, safe=False)
