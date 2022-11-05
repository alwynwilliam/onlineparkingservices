from django.shortcuts import render


from django.views import generic as views
from core import models as core_models
from core.forms import FeedbackForm
from django.urls import reverse_lazy


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

# feedback createview
class FeedbackCreateView(views.CreateView):
    template_name = "core/feedback_create.html"
    form_class = FeedbackForm
    success_url = reverse_lazy("core:home")

# feedback listview
class FeedbackListView(views.ListView):
    template_name = "core/feedback_list.html"
    model = core_models.FeedbackModel
    context_object_name ="feedbacks"

class ProfileView(views.TemplateView):
    template_name = "core/profile.html"

class ProfileEditView(views.TemplateView):
    template_name = "core/profile_edit.html"
    
class MyActivityView(views.TemplateView):
    template_name = "core/my_activity.html"
    
