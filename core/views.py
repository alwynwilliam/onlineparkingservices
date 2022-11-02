from django.shortcuts import render


from django.views import generic as views

# ========================================== Home view ============================================

class HomeView(views.TemplateView):
    template_name = "core/home.html"
    extra_context = {
        
    }

class AboutView(views.TemplateView):
    template_name = "core/about.html"

class LocationView(views.TemplateView):
    template_name = "core/location.html"
    
class TimeView(views.TemplateView):
    template_name = "core/time.html"
    
class BookingView(views.TemplateView):
    template_name = "core/booking.html"