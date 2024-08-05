from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from .forms import ContactForm
from .models import ContactRequest


@method_decorator(login_required, name="dispatch")
class ContactCreateView(CreateView):
    """A view for creating contact requests."""

    model = ContactRequest
    form_class = ContactForm
    template_name = "contact/contact_form.html"
    success_url = "/contact/success/"

    def form_valid(self, form):
        """If the form is valid, set the user and save the form."""
        form.instance.user = self.request.user
        messages.success(
            self.request, "Your contact request has been submitted successfully."
        )
        return super().form_valid(form)

    def get_initial(self):
        """Get initial data for the contact form."""
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial["email"] = self.request.user.email
        return initial


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """A view for updating contact requests."""

    model = ContactRequest
    form_class = ContactForm
    template_name = "contact/edit_contact_request.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        """Allow staff to edit any request, and users to edit their own requests."""
        contact_request = self.get_object()
        return self.request.user.is_staff or contact_request.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("dashboard")

    def form_valid(self, form):
        messages.success(
            self.request, "The contact request has been updated successfully."
        )
        return super().form_valid(form)


class ContactDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """A view for deleting contact requests."""

    model = ContactRequest
    template_name = "contact/delete_contact_request.html"
    success_url = reverse_lazy("dashboard")

    def test_func(self):
        """Allow staff to delete any request, and users to delete their own requests."""
        contact_request = self.get_object()
        return self.request.user.is_staff or contact_request.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("dashboard")

    def delete(self, request, *args, **kwargs):
        messages.success(
            self.request, "The contact request has been deleted successfully."
        )
        return super().delete(request, *args, **kwargs)
