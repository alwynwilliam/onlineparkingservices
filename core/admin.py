from django.contrib import admin
from core import models

admin.site.register(models.FeedbackModel)
admin.site.register(models.LocationModel)
admin.site.register(models.VehicleTypeModel)
admin.site.register(models.VehicleModel)
admin.site.register(models.SlotModel)
admin.site.register(models.ImageModel)
admin.site.register(models.DestinationModel)
admin.site.register(models.BookingModel)
admin.site.register(models.PaymentModel)

