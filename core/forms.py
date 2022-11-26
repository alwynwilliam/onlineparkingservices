from django import forms

from core import models


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackModel
        exclude = ("status",)


class DestinationForm(forms.ModelForm):
    class Meta:
        model = models.DestinationModel
        fields = [
            "name",
            "description",
            "location",
            "image",
            "slots",
        ]


class LocationForm(forms.ModelForm):
    class Meta:
        model = models.LocationModel
        exclude = ("status",)


class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        qs = models.VehicleModel.objects.filter(created_by=request.user)
        self.fields["vehicle"] = forms.ModelChoiceField(queryset=qs)

    class Meta:
        model = models.BookingModel
        fields = [
            "destination",
            "vehicle",
            "arrival_date",
            "departure_date",
        ]
        widgets = {
            "arrival_date": forms.DateInput(attrs={"type": "datetime-local"}),
            "departure_date": forms.DateInput(attrs={"type": "datetime-local"}),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = models.VehicleModel
        fields = [
            "model_name",
            "registration_number",
            "brand",
            "type",
        ]


class PaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        booking_pk = kwargs.pop("booking_pk")
        super().__init__(*args, **kwargs)
        booking_qs = models.BookingModel.objects.filter(id=booking_pk)
        booking_obj = booking_qs.first()
        payment_obj = models.PaymentModel.objects.filter(booking=booking_obj).first()
        amount = booking_obj.slot.amount
        self.fields["booking"] = forms.ModelChoiceField(queryset=booking_qs, initial=booking_obj)
        self.fields["amount"] = forms.IntegerField(
            widget=forms.NumberInput(attrs={"readonly": "true"}),
            initial=amount,
        )
        if payment_obj:
            self.instance = payment_obj

    class Meta:
        model = models.PaymentModel
        fields = [
            "booking",
            "amount",
        ]
