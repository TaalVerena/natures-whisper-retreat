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


@method_decorator(login_required, name="dispatch")
class ContactCreateView(CreateView):
    model = ContactRequest
    form_class = ContactForm
    template_name = "contact/contact_form.html"
    success_url = reverse_lazy("contact_success")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Explicitly set status to 'pending' if not specified
        if not form.instance.status:
            form.instance.status = 'pending'

        messages.success(self.request, "Your contact request has been submitted successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)


class ContactUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating contact requests.
    """

    model = ContactRequest
    form_class = ContactForm
    template_name = "contact/edit_contact_request.html"

    def get_form_kwargs(self):
        """
        Pass the request user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def test_func(self):
        """
        Ensure user has permission to edit the contact request.
        """
        contact_request = self.get_object()
        return self.request.user.is_staff or contact_request.user == self.request.user

    def handle_no_permission(self):
        """
        Handle lack of permission with a message and redirect.
        """
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("dashboard")

    def form_valid(self, form):
        """
        Save form and show success message if valid.
        """
        messages.success(
            self.request, "The contact request has been updated successfully."
        )
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect staff to reservation list, users to dashboard.
        """
        if self.request.user.is_staff:
            return reverse_lazy("reservation_list")
        return reverse_lazy("dashboard")


class ContactDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting contact requests.
    """

    model = ContactRequest
    template_name = "contact/delete_contact_request.html"

    def test_func(self):
        """
        Allow staff to delete any request, users to delete their own.
        """
        contact_request = self.get_object()
        return self.request.user.is_staff or contact_request.user == self.request.user

    def handle_no_permission(self):
        """
        Handle lack of permission with a message and redirect.
        """
        messages.error(self.request, "You do not have permission to access this page.")
        return redirect("dashboard")

    def delete(self, request, *args, **kwargs):
        """
        Delete contact request and show success message.
        """
        messages.success(
            self.request, "The contact request has been deleted successfully."
        )
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        """
        Redirect staff to reservation list, users to dashboard.
        """
        if self.request.user.is_staff:
            return reverse_lazy("reservation_list")
        return reverse_lazy("dashboard")
