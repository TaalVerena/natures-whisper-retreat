from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
from reservations.models import Reservation
from contact.forms import ContactForm


@login_required
def dashboard(request):
    """
    Render user reservations and contact form.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML template for the user dashboard.
    """
    # Get the authenticated user
    user = request.user

    # Get the current date
    current_date = datetime.now().date()

    # Retrieve upcoming reservations for the user
    upcoming_reservations = Reservation.objects.filter(
        user=user, start_date__gte=current_date, status=Reservation.Status.CONFIRMED
    ).order_by("start_date")

    # Retrieve past reservations for the user
    past_reservations = Reservation.objects.filter(
        user=user, start_date__lt=current_date, status=Reservation.Status.CONFIRMED
    ).order_by("-start_date")

    # Instantiate a contact form for the user
    contact_form = ContactForm()

    # Prepare the context data to be passed to the template
    context = {
        "upcoming_reservations": upcoming_reservations,
        "past_reservations": past_reservations,
        "contact_form": contact_form,
    }

    # Render the dashboard template with the context data
    return render(request, "dashboard/dashboard.html", context)
