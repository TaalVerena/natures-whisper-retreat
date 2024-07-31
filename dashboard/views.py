from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from datetime import datetime
from reservations.models import Reservation
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
    Display a list of reservations for staff users.
    """
    reservations = Reservation.objects.all().order_by("-start_date")
    return render(
        request, "dashboard/reservation_list.html", {"reservations": reservations}
    )
