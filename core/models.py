from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.conf import settings


USER = settings.AUTH_USER_MODEL


class TimeStamp(models.Model):
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#recommonded places


# feedback model
class FeedbackModel(TimeStamp, models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField()
    subject = models.CharField(max_length=120)
    message = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name}"


# location model/category
class LocationModel(TimeStamp, models.Model):
    name = models.CharField(max_length=128, default="unknown", blank=True)
    lattitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.lattitude},{self.longitude}"


class ImageModel(models.Model):
    file = models.ImageField(
        upload_to="destination/image/", default="default/destination.png"
    )

    def __str__(self) -> str:
        return f"{self.file.path}"


# Vehicle Model
class VehicleTypeModel(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


# Vehicle Model
class VehicleModel(models.Model):
    model_name = models.CharField(max_length=64)
    registration_number = models.CharField(max_length=64)
    brand = models.CharField(max_length=64)
    type = models.ForeignKey(
        VehicleTypeModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, blank=True, null=True
    )
    

    def __str__(self):
        return f"{self.registration_number} {self.type}"


# Slot Model
class SlotModel(models.Model):
    filled = models.BooleanField(default=False)
    vehicle_type = models.ForeignKey(VehicleTypeModel, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        availability = "Avaible" if not self.filled else "Not Available"
        return f"{self.vehicle_type} ({availability})"


# destination/product
class DestinationModel(TimeStamp, models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=500)
    location = models.ForeignKey(
        LocationModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    image = models.ManyToManyField(ImageModel)
    slots = models.ManyToManyField(SlotModel)
    created_by = models.ForeignKey(
        USER, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("core:destination_detail", kwargs={"id":self.id})


# booking model
class BookingModel(TimeStamp, models.Model):
    USER = get_user_model()

    destination = models.ForeignKey(DestinationModel, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    arrival_date = models.DateTimeField()
    departure_date = models.DateTimeField()
    slot = models.ForeignKey(SlotModel, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.destination} ({self.arrival_date})"

    def get_absolute_url(self):
        return reverse("core:booking_detail", kwargs={"pk":self.id})

    def available_slots(self):
        slots = self.destination.slots.filter(filled=False)
        return slots

    def fill_slot(self):
        slot = self.available_slots().first()
        if slot:
            slot.filled = True

# Payment Model
class PaymentModel(TimeStamp, models.Model):
    booking = models.OneToOneField(BookingModel, on_delete=models.SET_DEFAULT, default=None)
    amount = models.FloatField(default=0.0)
    ispaid = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=256)
    payment_method = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.booking} (RS.{self.amount}/-)"

    def get_absolute_url(self):
        return reverse("core:payment_detail", kwargs={"id":self.id})
