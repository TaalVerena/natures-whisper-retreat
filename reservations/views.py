from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .forms import ReservationForm
from lodges.models import Lodge
from .models import Reservation
import datetime


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
    try:
        reservations = Reservation.objects.filter(lodge_id=lodge_id)
        events = []
        for reservation in reservations:
            events.append({
                'title': f"Booked: {reservation.guests} guests",
                'start': reservation.start_date.strftime('%Y-%m-%d'),
                'end': (reservation.end_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                'rendering': 'background',
                'color': '#ff9f89'
            })
        return JsonResponse(events, safe=False)
    except Exception as e:
        print("Error fetching events:", e)
        return JsonResponse({'error': 'An error occurred'}, status=500)
