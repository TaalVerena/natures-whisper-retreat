from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.dateparse import parse_date
from .forms import ReservationForm
from lodges.models import Lodge
from .models import Reservation
from datetime import datetime, date, timedelta


# Create your views here.
@login_required
def make_reservation(request, lodge_id):
    lodge = get_object_or_404(Lodge, pk=lodge_id)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.lodge = lodge
            reservation.user = request.user
            reservation.rate = lodge.rate
            reservation.save()
            messages.success(request, "Reservation successful!")
            return redirect("reservation_confirmation", reservation.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReservationForm()

    return render(
        request, "reservations/make_reservation.html", {"form": form, "lodge": lodge}
    )

def reservation_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservations/reservation_confirmation.html', {'reservation': reservation})

def calendar_events(request, lodge_id):
    lodge = get_object_or_404(Lodge, pk=lodge_id)
    start_date = date.today() 
    end_date = start_date + timedelta(days=90)

    reservations = Reservation.objects.filter(lodge_id=lodge_id, start_date__lte=end_date, end_date__gte=start_date)

    booked_dates = set()
    for reservation in reservations:
        delta = reservation.end_date - reservation.start_date
        for i in range(delta.days + 1):
            day = reservation.start_date + timedelta(days=i)
            booked_dates.add(day.strftime('%Y-%m-%d'))

    events = []
    for day in booked_dates:
        events.append({
            'title': "Fully Booked",
            'start': day,
            'end': day,
            'color': '#ff9f89',
            'textColor': '#000000',
            'allDay': True,
            'type': 'booked'
        })

    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime('%Y-%m-%d') not in booked_dates:
            events.append({
                'title': f"Rate: ${lodge.rate}",
                'start': current_date.strftime('%Y-%m-%d'),
                'end': current_date.strftime('%Y-%m-%d'),
                'color': '#ccffcc', 
                'textColor': '#000000',
                'allDay': True,
                'type': 'rate'
            })
        current_date += timedelta(days=1)

    return JsonResponse(events, safe=False)

def get_booked_dates(request, lodge_id):
    today = datetime.today()
    end_date = today + timedelta(days=90)

    reservations = Reservation.objects.filter(lodge_id=lodge_id, start_date__lte=end_date, end_date__gte=today)
    booked_dates = {reservation.start_date.strftime('%Y-%m-%d') for reservation in reservations for _ in range((reservation.end_date - reservation.start_date).days + 1)}

    return JsonResponse(list(booked_dates), safe=False)