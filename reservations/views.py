from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .forms import ReservationForm
from lodges.models import Lodge
from .models import Reservation
import datetime

# Create your views here.
def make_reservation(request, lodge_id):
    lodge = get_object_or_404(Lodge, pk=lodge_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.lodge = lodge
            reservation.user = request.user
            reservation.save()
            return redirect('reservation_confirmation', reservation.id) 
    else:
        form = ReservationForm()

    return render(request, 'reservations/make_reservation.html', {
        'form': form,
        'lodge': lodge
    })

def calendar_events(request, lodge_id):
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