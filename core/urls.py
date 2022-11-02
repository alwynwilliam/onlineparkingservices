from django.urls import path

from core import views

app_name = "core"


urlpatterns=[
     path("", views.HomeView.as_view(), name="home"),
     path("about/", views.AboutView.as_view(), name="about"),
     path("location/", views.LocationView.as_view(), name="location"),
     path("time/", views.TimeView.as_view(), name="time"),
     path("booking/", views.BookingView.as_view(), name="booking"),
    
]