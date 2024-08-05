# views.py

from django.views.generic.edit import CreateView
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from .forms import ContactForm
from .models import ContactRequest


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    """A view for creating contact requests."""

    model = ContactRequest
    form_class = ContactForm
    template_name = "contact/contact_form.html"
    success_url = "/contact/success/"

    def form_valid(self, form):
        """If the form is valid, set the user and save the form."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        """Get initial data for the contact form."""
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["email"] = self.request.user.email
        return initial


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ContactRequest
    form_class = ContactForm
    template_name = "contact/edit_contact_request.html"
    success_url = reverse_lazy("dashboard") 

    def test_func(self):
        """Check if the logged-in user is the owner of the contact request."""
        contact_request = self.get_object()
        return contact_request.user == self.request.user

    def handle_no_permission(self):
        """Handle the case where a user does not have permission to edit."""
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("dashboard")


@method_decorator(login_required, name='dispatch')
class ContactDeleteView(DeleteView):
    model = ContactRequest
    template_name = 'contact/delete_contact_request.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        """Ensure a user can only delete their own queries."""
        return ContactRequest.objects.filter(user=self.request.user)