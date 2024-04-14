from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReservationForm
from lodges.models import Lodge

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