from django.urls import path

from core import views

app_name = "core"


urlpatterns=[
     path("", views.HomeView.as_view(), name="home"),
     path("about/", views.AboutView.as_view(), name="about"),
     path("location/", views.LocationView.as_view(), name="location"),
     path("time/", views.TimeView.as_view(), name="time"),
     path("booking/", views.BookingView.as_view(), name="booking"),
     path("feedback_create/", views.FeedbackCreateView.as_view(), name="feedback_create"),
     path("feedback_list/", views.FeedbackListView.as_view(), name="feedback_list"),
     path("profile/", views.ProfileView.as_view(), name="profile"),
     path("profile_edit/", views.ProfileEditView.as_view(), name="profile_edit"),
    
]