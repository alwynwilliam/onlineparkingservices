# Generated by Django 4.1.2 on 2022-11-17 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BookingModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("arrival_date", models.DateTimeField()),
                ("departure_date", models.DateTimeField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FeedbackModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=64)),
                ("email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=120)),
                ("message", models.TextField(max_length=500)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ImageModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.ImageField(
                        default="default/destination.png",
                        upload_to="destination/image/",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LocationModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("lattitude", models.FloatField()),
                ("longitude", models.FloatField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="VehicleTypeModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name="VehicleModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("model_name", models.CharField(max_length=64)),
                ("registration_number", models.CharField(max_length=64)),
                ("brand", models.CharField(max_length=64)),
                (
                    "type",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.vehicletypemodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SlotModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("filled", models.BooleanField(default=False)),
                (
                    "vehicle_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.vehicletypemodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PaymentModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                ("ispaid", models.BooleanField(default=False)),
                ("payment_id", models.CharField(max_length=256)),
                ("payment_method", models.CharField(max_length=64)),
                (
                    "booking",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="core.bookingmodel",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DestinationModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("status", models.BooleanField(default=True)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=64)),
                ("description", models.TextField(max_length=500)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("image", models.ManyToManyField(to="core.imagemodel")),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="core.locationmodel",
                    ),
                ),
                ("slots", models.ManyToManyField(to="core.slotmodel")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="bookingmodel",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.destinationmodel"
            ),
        ),
        migrations.AddField(
            model_name="bookingmodel",
            name="slot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.slotmodel"
            ),
        ),
        migrations.AddField(
            model_name="bookingmodel",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="bookingmodel",
            name="vehicle",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.vehiclemodel"
            ),
        ),
    ]
