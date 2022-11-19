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
    # arrival_date = forms.DateTimeField(wi)
    # departure_date = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        qs = models.VehicleModel.objects.filter(created_by=request.user)
        print(qs)
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
