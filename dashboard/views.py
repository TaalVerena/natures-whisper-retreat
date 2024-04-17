from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from reservations.models import Reservation
from contact.forms import ContactForm

# Create your views here.

@login_required
def dashboard(request):
    user = request.user
    current_date = datetime.now().date()
    upcoming_reservations = Reservation.objects.filter(user=user, start_date__gte=current_date).order_by('start_date')
    past_reservations = Reservation.objects.filter(user=user, start_date__lt=current_date).order_by('-start_date')

    contact_form = ContactForm()

    context = {
        'upcoming_reservations': upcoming_reservations,
        'past_reservations': past_reservations,
        'contact_form': contact_form,
    }
    return render(request, 'dashboard/dashboard.html', context)
