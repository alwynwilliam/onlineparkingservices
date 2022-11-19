from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from core import forms as core_forms
from core import models as core_models
from core.forms import FeedbackForm

# home view


class HomeView(views.TemplateView):
    template_name = "core/home.html"


# about view
class AboutView(views.TemplateView):
    template_name = "core/about.html"


# feedback createview
class FeedbackCreateView(views.CreateView):
    template_name = "core/feedback_create.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("core:home")


# feedback listview
class FeedbackListView(views.ListView):
    template_name = "core/feedback_list.html"
    model = core_models.FeedbackModel
    context_object_name = "feedbacks"


# Location List
class LocationListView(views.ListView):
    template_name = "core/location/list.html"
    model = core_models.LocationModel
    context_object_name = "locations"

    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     pk = self.kwargs.get("pk", None)
    #     qs = qs.filter(location__id=pk)
    #     return qs


# Destination
class DestinationListView(views.ListView):
    template_name = "core/destination/list.html"
    model = core_models.DestinationModel
    context_object_name = "destinations"


class DestinationByLocationView(views.ListView):
    template_name = "core/destination/list.html"
    model = core_models.DestinationModel
    context_object_name = "destinations"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        pk = self.kwargs.get("pk", None)
        qs = qs.filter(location__id=pk)
        return qs


class DestinationSearchView(views.ListView):
    template_name = "core/destination/list.html"
    model = core_models.DestinationModel
    context_object_name = "destinations"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get("q", None)
        qs = qs.filter(Q(name__icontains=q) | Q(location__name__icontains=q))
        return qs


# Booking
class BookingCreateView(LoginRequiredMixin, SuccessMessageMixin, views.CreateView):
    template_name = "core/booking/form.html"
    model = core_models.BookingModel
    form_class = core_forms.BookingForm
    extra_context = {"vehicle_form": core_forms.VehicleForm}

    def form_valid(self, form):
        slot = core_models.SlotModel.objects.filter().first()
        form.instance.slot = slot
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"request": self.request})
        return kwargs


class BookingListView(LoginRequiredMixin, views.ListView):
    template_name = "core/booking/list.html"
    model = core_models.BookingModel
    context_object_name = "bookings"


class BookingDetailView(LoginRequiredMixin, views.DetailView):
    template_name = "core/booking/detail.html"
    model = core_models.BookingModel
    context_object_name = "booking"


class BookingUpdateView(LoginRequiredMixin, SuccessMessageMixin, views.UpdateView):
    template_name = "core/booking/form.html"
    model = core_models.BookingModel
    form_class = core_forms.BookingForm


class BookingDeleteView(LoginRequiredMixin, SuccessMessageMixin, views.DeleteView):
    template_name = "core/booking/delete.html"
    model = core_models.BookingModel
    success_url = reverse_lazy("core:home")


class VehicleCreateView(LoginRequiredMixin, SuccessMessageMixin, views.CreateView):
    template_name = "core/vehicle/form.html"
    form_class = core_forms.VehicleForm
    success_message = "Vehicle created successfully!"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        url = self.request.META.get("HTTP_REFERER")
        return url


class PaymentView(LoginRequiredMixin, SuccessMessageMixin, views.CreateView):
    template_name = "core/payment.html"
    model = core_models.PaymentModel


# # -----------------------location and destination------------------------------------
# class LocationView(views.ListView):
#     template_name = "core/location.html"
#     model = core_models.LocationModel
#     context_object_name = "locations"

# class DestinationListView(views.ListView):
#     template_name = "core/destination.html"
#     model = core_models.DestinationModel
#     context_object_name = "destinations"

#
