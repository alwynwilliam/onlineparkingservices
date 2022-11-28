from django.urls import path

from core import views

app_name = "core"


urlpatterns=[
     path("", views.HomeView.as_view(), name="home"),
     
     path("about/", views.AboutView.as_view(), name="about"),

     # Feedback
     path("feedback_create/", views.FeedbackCreateView.as_view(), name="feedback_create"),
     path("feedback_list/", views.FeedbackListView.as_view(), name="feedback_list"),

     # Location
     path("location/list/", views.LocationListView.as_view(), name="location_list"),

     # Booking
     path("booking/create/", views.BookingCreateView.as_view(), name="booking_create"),
     path("destination/<int:pk>/book_slot/", views.BookingCreateView.as_view(), name="booking_create"),
     path("booking/list/", views.BookingListView.as_view(), name="booking_list"),
     path("booking/<int:pk>/detail/", views.BookingDetailView.as_view(), name="booking_detail"),
     path("booking/<int:pk>/update/", views.BookingUpdateView.as_view(), name="booking_update"),
     path("booking/<int:pk>/delete/", views.BookingDeleteView.as_view(), name="booking_delete"),
     path("booking/<int:pk>/payment/", views.BookingPaymentView.as_view(), name="booking_payment"),

     #my activity
     path("myactivity/list/", views.MyactivityListView.as_view(), name="my_activity"),

     #vehicle
    path("vehicle/create/", views.VehicleCreateView.as_view(), name="vehicle_create"),

     # Destination
     path("destination/list/",views.DestinationListView.as_view(), name="destination_list"),
     path("destination/location/<int:pk>/list/",views.DestinationByLocationView.as_view(),name="destination_by_location"),
     path("destination/search/",views.DestinationSearchView.as_view(),name="destination_search"),
     # Payment
     path("payment/<int:pk>/",views.PaymentHandler.as_view(),name="payment_handler"),


    

     
    
]