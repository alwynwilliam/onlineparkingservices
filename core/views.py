import razorpay
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from core import forms as core_forms
from core import models as core_models
from core.forms import FeedbackForm


# home view


class HomeView(views.TemplateView):
    template_name = "core/home.html"
    extra_context = {"destinations": core_models.DestinationModel.objects.filter(status=True)}

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
        pk = self.kwargs.get("pk", None)

        if pk:
            destination = core_models.DestinationModel.objects.get(id=pk)
            kwargs.update({"initial": {"destination": destination}})
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


class MyactivityListView(LoginRequiredMixin, views.ListView):
    template_name = "core/myactivity.html"
    model = core_models.BookingModel
    context_object_name = "bookings"




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


class BookingPaymentView(LoginRequiredMixin, SuccessMessageMixin, views.View):
    template_name = "core/booking/payment.html"
    model = core_models.PaymentModel
    form_class = core_forms.PaymentForm
    success_message = "Payment done successfully!"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        form = self.form_class(booking_pk=pk)
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, booking_pk=kwargs.get("pk"))
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect(self.get_success_url())

    def get_success_url(self) -> str:
        pk = self.object.id
        url = reverse_lazy("core:payment_handler", kwargs={"pk": pk})
        return url



class PaymentView(views.View):
    def get(self, request):

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        payment = client.Order.create(  # type: ignore
            {"amount": 10000, "currency": "INR", "payment_capture": "1"}
        )


class PaymentHandler(views.View):
    template_name = "core/payment.html"

    def get(self, request, *args, **kwargs):
        # payment here
        pk = kwargs.get("pk")
        payment = core_models.PaymentModel.objects.get(id=pk)
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        data = {
            "amount": payment.amount,
            "currency": "INR",
            "receipt": payment.id,
            "payment_capture": 1,
        }
        order = client.order.create(data=data)
        context = {}
        context.update(order)
        return render(request, self.template_name, context) 

    
    def post(self, request, *args, **kwargs):
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get("razorpay_payment_id", "")
            amount = request.POST.get("razorpay_amount", "0")
            razorpay_order_id = request.POST.get("razorpay_order_id", "")
            signature = request.POST.get("razorpay_signature", "")

            params_dict = {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            }
            print("#DEBUG: Amount", type(amount), amount)
            try:
                amount = int(float(amount))
            except Exception as e:
                print("#DEBUG: amount can be converted into integer", e)
                amount = 5000
            print("#DEBUG: verifying the payment signature...", params_dict, amount)

            # verify the payment signature.
            result = self.RAZORPAY_CLIENT.utility.verify_payment_signature(params_dict)
            print("#DEBUG: verifying the payment signature... Completed.") 

            if result is not None:

                try:
                    print("#DEBUG: Payment capturing...")
                    # capture the payment
                    self.RAZORPAY_CLIENT.payment.capture(payment_id, amount)
                    print("#DEBUG: Payment captured...")
                    print("#DEBUG: Payment model creating...")

                    core_models.Payment.objects.create(
                        razorpay_order_id=razorpay_order_id,
                        razorpay_payment_id=payment_id,
                        status=core_models.Payment.PaymentStatusChoices.completed,
                        mode="",
                    )
                    print("#DEBUG: Payment model created...")


                    # render success page on successful caputre of payment
                    return render(request, "core/paymentsuccess.html")
                except Exception as e:
                    print("#DEBUG: there is an error while capturing payment...", e)
                    
                    # if there is an error while capturing payment.
                    return render(request, "core/paymentfail.html")
            else:
                print("#DEBUG: signature verification failed...", e)
                # if signature verification fails.
                return render(request, "core/paymentfail.html")
        except Exception as e:
            print("#DEBUG: we don't find the required parameters in POST data", e)
            # if we don't find the required parameters in POST data
            return redirect(reverse_lazy("core:payment_completed", kwargs={"pk":self.kwargs.get("pk")}))







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
